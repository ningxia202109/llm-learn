from autogen_core.base import MessageContext, TopicId
from autogen_core.components import RoutedAgent, default_subscription, message_handler
from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_ext.models import OpenAIChatCompletionClient
from typing import Dict, List, Union

from src.models import CodeReviewTask, CodeReviewResult, CodeWritingTask, CodeWritingResult

system_prompt = f"""
You are an expert Python programmer specializing in data processing and analysis. Your main responsibilities include:

1. Writing clean, efficient Python code for data manipulation, cleaning, and transformation.
2. Implementing statistical methods and machine learning algorithms as needed.
3. Debugging and optimizing existing code for performance improvements.
4. Adhering to PEP 8 standards and ensuring code readability with meaningful variable and function names.

Constraints:
- Focus solely on data processing tasks; do not generate visualizations or write non-Python code.
- Provide only valid, executable Python code, including necessary comments for complex logic.
- Avoid unnecessary complexity; prioritize readability and efficiency.
"""


class CoderAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("A python writing agent.")
        self._system_messages: List[LLMMessage] = [SystemMessage(content=system_prompt)]
        self.model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
        self._session_memory: Dict[
            str, List[CodeWritingTask | CodeReviewTask | CodeReviewResult]
        ] = {}

    @message_handler
    async def handle_code_writing_task(
        self, message: CodeWritingTask, ctx: MessageContext
    ) -> None:
        session_id = str(uuid.uuid4())
        self._session_memory.setdefault(session_id, []).append(message)
        # Generate a response using the chat completion API.
        response = await self._model_client.create(
            self._system_messages
            + [UserMessage(content=message.task, source=self.metadata["type"])],
            cancellation_token=ctx.cancellation_token,
        )
        assert isinstance(response.content, str)
        # Extract the code block from the response.
        code_block = self._extract_code_block(response.content)
        if code_block is None:
            raise ValueError("Code block not found.")
        # Create a code review task.
        code_review_task = CodeReviewTask(
            session_id=session_id,
            code_writing_task=message.task,
            code_writing_scratchpad=response.content,
            code=code_block,
        )
        # Store the code review task in the session memory.
        self._session_memory[session_id].append(code_review_task)
        # Publish a code review task.
        await self.publish_message(
            code_review_task, topic_id=TopicId("default", self.id.key)
        )


