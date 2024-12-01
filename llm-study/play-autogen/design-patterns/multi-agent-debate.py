# https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/design-patterns/multi-agent-debate.html

import asyncio
import re
from dataclasses import dataclass
from typing import Dict, List

from autogen_core.application import SingleThreadedAgentRuntime
from autogen_core.base import MessageContext
from autogen_core.components import (
    DefaultTopicId,
    RoutedAgent,
    TypeSubscription,
    default_subscription,
    message_handler,
)
from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    OpenAIChatCompletionClient,
    SystemMessage,
    UserMessage,
)


@dataclass
class Question:
    content: str


@dataclass
class Answer:
    content: str


@dataclass
class SolverRequest:
    content: str
    question: str


@dataclass
class IntermediateSolverResponse:
    content: str
    question: str
    answer: str
    round: int


@dataclass
class FinalSolverResponse:
    answer: str


@default_subscription
class MathSolver(RoutedAgent):
    def __init__(
        self,
        model_client: ChatCompletionClient,
        topic_type: str,
        num_neighbors: int,
        max_round: int,
    ) -> None:
        super().__init__("A debator.")
        self._topic_type = topic_type
        self._model_client = model_client
        self._num_neighbors = num_neighbors
        self._history: List[LLMMessage] = []
        self._buffer: Dict[int, List[IntermediateSolverResponse]] = {}
        self._system_messages = [
            SystemMessage(
                (
                    "You are a helpful assistant with expertise in mathematics and reasoning. "
                    "Your task is to assist in solving a math reasoning problem by providing "
                    "a clear and detailed solution. Limit your output within 100 words, "
                    "and your final answer should be a single numerical number, "
                    "in the form of {{answer}}, at the end of your response. "
                    "For example, 'The answer is {{42}}.'"
                )
            )
        ]
        self._round = 0
        self._max_round = max_round

    @message_handler
    async def handle_request(self, message: SolverRequest, ctx: MessageContext) -> None:
        # Add the question to the memory.
        self._history.append(UserMessage(content=message.content, source="user"))
        # Make an inference using the model.
        model_result = await self._model_client.create(
            self._system_messages + self._history
        )
        assert isinstance(model_result.content, str)
        # Add the response to the memory.
        self._history.append(
            AssistantMessage(content=model_result.content, source=self.metadata["type"])
        )
        print(
            f"{'-'*80}\nSolver {self.id} round {self._round}:\n{model_result.content}"
        )
        # Extract the answer from the response.
        match = re.search(r"\{\{(\-?\d+(\.\d+)?)\}\}", model_result.content)
        if match is None:
            raise ValueError("The model response does not contain the answer.")
        answer = match.group(1)
        # Increment the counter.
        self._round += 1
        if self._round == self._max_round:
            # If the counter reaches the maximum round, publishes a final response.
            await self.publish_message(
                FinalSolverResponse(answer=answer), topic_id=DefaultTopicId()
            )
        else:
            # Publish intermediate response to the topic associated with this solver.
            await self.publish_message(
                IntermediateSolverResponse(
                    content=model_result.content,
                    question=message.question,
                    answer=answer,
                    round=self._round,
                ),
                topic_id=DefaultTopicId(type=self._topic_type),
            )

    @message_handler
    async def handle_response(
        self, message: IntermediateSolverResponse, ctx: MessageContext
    ) -> None:
        # Add neighbor's response to the buffer.
        self._buffer.setdefault(message.round, []).append(message)
        # Check if all neighbors have responded.
        if len(self._buffer[message.round]) == self._num_neighbors:
            print(
                f"{'-'*80}\nSolver {self.id} round {message.round}:\nReceived all responses from {self._num_neighbors} neighbors."
            )
            # Prepare the prompt for the next question.
            prompt = "These are the solutions to the problem from other agents:\n"
            for resp in self._buffer[message.round]:
                prompt += f"One agent solution: {resp.content}\n"
            prompt += (
                "Using the solutions from other agents as additional information, "
                "can you provide your answer to the math problem? "
                f"The original math problem is {message.question}. "
                "Your final answer should be a single numerical number, "
                "in the form of {{answer}}, at the end of your response."
            )
            # Send the question to the agent itself to solve.
            await self.send_message(
                SolverRequest(content=prompt, question=message.question), self.id
            )
            # Clear the buffer.
            self._buffer.pop(message.round)


@default_subscription
class MathAggregator(RoutedAgent):
    def __init__(self, num_solvers: int) -> None:
        super().__init__("Math Aggregator")
        self._num_solvers = num_solvers
        self._buffer: List[FinalSolverResponse] = []

    @message_handler
    async def handle_question(self, message: Question, ctx: MessageContext) -> None:
        print(f"{'-'*80}\nAggregator {self.id} received question:\n{message.content}")
        prompt = (
            f"Can you solve the following math problem?\n{message.content}\n"
            "Explain your reasoning. Your final answer should be a single numerical number, "
            "in the form of {{answer}}, at the end of your response."
        )
        print(f"{'-'*80}\nAggregator {self.id} publishes initial solver request.")
        await self.publish_message(
            SolverRequest(content=prompt, question=message.content),
            topic_id=DefaultTopicId(),
        )

    @message_handler
    async def handle_final_solver_response(
        self, message: FinalSolverResponse, ctx: MessageContext
    ) -> None:
        self._buffer.append(message)
        if len(self._buffer) == self._num_solvers:
            print(
                f"{'-'*80}\nAggregator {self.id} received all final answers from {self._num_solvers} solvers."
            )
            # Find the majority answer.
            answers = [resp.answer for resp in self._buffer]
            majority_answer = max(set(answers), key=answers.count)
            # Publish the aggregated response.
            await self.publish_message(
                Answer(content=majority_answer), topic_id=DefaultTopicId()
            )
            # Clear the responses.
            self._buffer.clear()
            print(
                f"{'-'*80}\nAggregator {self.id} publishes final answer:\n{majority_answer}"
            )


async def main() -> None:
    runtime = SingleThreadedAgentRuntime()
    await MathSolver.register(
        runtime,
        "MathSolverA",
        lambda: MathSolver(
            model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
            topic_type="MathSolverA",
            num_neighbors=2,
            max_round=3,
        ),
    )
    await MathSolver.register(
        runtime,
        "MathSolverB",
        lambda: MathSolver(
            model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
            topic_type="MathSolverB",
            num_neighbors=2,
            max_round=3,
        ),
    )
    await MathSolver.register(
        runtime,
        "MathSolverC",
        lambda: MathSolver(
            model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
            topic_type="MathSolverC",
            num_neighbors=2,
            max_round=3,
        ),
    )
    await MathSolver.register(
        runtime,
        "MathSolverD",
        lambda: MathSolver(
            model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
            topic_type="MathSolverD",
            num_neighbors=2,
            max_round=3,
        ),
    )
    await MathAggregator.register(
        runtime, "MathAggregator", lambda: MathAggregator(num_solvers=4)
    )

    # Subscriptions for topic published to by MathSolverA.
    await runtime.add_subscription(TypeSubscription("MathSolverA", "MathSolverD"))
    await runtime.add_subscription(TypeSubscription("MathSolverA", "MathSolverB"))

    # Subscriptions for topic published to by MathSolverB.
    await runtime.add_subscription(TypeSubscription("MathSolverB", "MathSolverA"))
    await runtime.add_subscription(TypeSubscription("MathSolverB", "MathSolverC"))

    # Subscriptions for topic published to by MathSolverC.
    await runtime.add_subscription(TypeSubscription("MathSolverC", "MathSolverB"))
    await runtime.add_subscription(TypeSubscription("MathSolverC", "MathSolverD"))

    # Subscriptions for topic published to by MathSolverD.
    await runtime.add_subscription(TypeSubscription("MathSolverD", "MathSolverC"))
    await runtime.add_subscription(TypeSubscription("MathSolverD", "MathSolverA"))

    # All solvers and the aggregator subscribe to the default topic.

    question = "Natalia sold clips to 48 of her friends in April, "
    "and then she sold half as many clips in May. ""How many clips did Natalia sell altogether in April and May?"
    runtime.start()
    await runtime.publish_message(Question(content=question), DefaultTopicId())
    await runtime.stop_when_idle()


asyncio.run(main())
