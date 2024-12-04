from autogen_core.base import MessageContext, TopicId
from autogen_core.components import RoutedAgent, default_subscription, message_handler
from autogen_core.components.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.components.tools import FunctionTool
from autogen_ext.models import OpenAIChatCompletionClient
from typing import Dict, List, Union
from typing import List

from src.tools import SwaggerAPIReader


system_prompt = f'''
You are a helpful assistant that can read and understand Swagger API specifications. Your main responsibilities include:
you use tool to read and understand Swagger API specifications,

'''

class SwaggerAgent(RoutedAgent):
    def __init__(self):
        super().__init__("Swagger Agent")
        self._system_messages: List[LLMMessage] = [
            SystemMessage(system_prompt)
        ]
        self._model_client = OpenAIChatCompletionClient(model="gpt-4o-mini"),
        self.tool = FunctionTool(get_stock_price, description="Get the stock price.")
        # self._tool_schema = tool_schema
        # self._tool_agent_id = AgentId(tool_agent_type, self.id.key)





