# Tools
# https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/framework/tools.html

import random

import asyncio

from autogen_core.base import CancellationToken
from typing_extensions import Annotated

from dataclasses import dataclass
from typing import List

from autogen_core.application import SingleThreadedAgentRuntime
from autogen_core.base import AgentId, AgentInstantiationContext, MessageContext
from autogen_core.components import RoutedAgent, message_handler
from autogen_core.components.models import (
    ChatCompletionClient,
    LLMMessage,
    OpenAIChatCompletionClient,
    SystemMessage,
    UserMessage,
)
from autogen_core.components.tool_agent import ToolAgent, tool_agent_caller_loop
from autogen_core.components.tools import FunctionTool, Tool, ToolSchema


async def get_stock_price(
    ticker: str, date: Annotated[str, "Date in YYYY/MM/DD"]
) -> float:
    # Returns a random stock price for demonstration purposes.
    return random.uniform(10, 200)


@dataclass
class Message:
    content: str


class ToolUseAgent(RoutedAgent):
    def __init__(
        self,
        model_client: ChatCompletionClient,
        tool_schema: List[ToolSchema],
        tool_agent_type: str,
    ) -> None:
        super().__init__("An agent with tools")
        self._system_messages: List[LLMMessage] = [
            SystemMessage("You are a helpful AI assistant.")
        ]
        self._model_client = model_client
        self._tool_schema = tool_schema
        self._tool_agent_id = AgentId(tool_agent_type, self.id.key)

    @message_handler
    async def handle_user_message(
        self, message: Message, ctx: MessageContext
    ) -> Message:
        # Create a session of messages.
        session: List[LLMMessage] = [
            UserMessage(content=message.content, source="user")
        ]
        # Run the caller loop to handle tool calls.
        messages = await tool_agent_caller_loop(
            self,
            tool_agent_id=self._tool_agent_id,
            model_client=self._model_client,
            input_messages=session,
            tool_schema=self._tool_schema,
            cancellation_token=ctx.cancellation_token,
        )
        # Return the final response.
        assert isinstance(messages[-1].content, str)
        return Message(content=messages[-1].content)


async def main() -> None:
    # Create a runtime.
    runtime = SingleThreadedAgentRuntime()
    # Create the tools.
    tools: List[Tool] = [
        FunctionTool(get_stock_price, description="Get the stock price.")
    ]
    # Register the agents.
    await ToolAgent.register(
        runtime, "tool_executor_agent", lambda: ToolAgent("tool executor agent", tools)
    )
    await ToolUseAgent.register(
        runtime,
        "tool_use_agent",
        lambda: ToolUseAgent(
            OpenAIChatCompletionClient(model="gpt-4o-mini"),
            [tool.schema for tool in tools],
            "tool_executor_agent",
        ),
    )

    # Start processing messages.
    runtime.start()
    # Send a direct message to the tool agent.
    tool_use_agent = AgentId("tool_use_agent", "default")
    response = await runtime.send_message(
        Message("What is the stock price of NVDA on 2024/06/01?"), tool_use_agent
    )
    print(response.content)
    # Stop processing messages.
    await runtime.stop()


# Run the main function

asyncio.run(main())
