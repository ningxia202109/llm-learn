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

from tools import SwaggerAPIReader


system_prompt = f'''
You are a helpful assistant that can read and understand Swagger API specifications. Your main responsibilities include:
you use tool to read and understand Swagger API specifications,

'''

class SwaggerAgent(RoutedAgent):
    def __init__(self, description):
        super().__init__(description)




