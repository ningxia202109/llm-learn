import asyncio
import os
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.base import CancellationToken


log_reader_system_prompt=r'''
you are a helpful assistant that can read log 
please follow ROLES to review log
<ROLES>
- privode ai analysis for each error
<\ROLES>
Response must follows SAMIPE_REPORT_FORMAT
<SAMIPE_REPORT_FORMAT>
{
    "summary": "<summary>",
    "errors": [
    {
        "timestamp": "2024-11-21 22:25:30",
        "error_type": "ZeroDivisionError",
        "message": "division by zero",
        "details": "/app/main.py, line 42, in create_item",
        "ai_analysis":"that is code issue",
    }
    ]
}
<\SAMIPE_REPORT_FORMAT>
'''

error_msg = """
[2024-11-21 22:25:30] ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/app/main.py", line 42, in create_item
    result = item.price / 0
ZeroDivisionError: division by zero

[2024-11-21 22:26:15] ERROR:    ValueError: Invalid input: Negative price not allowed
Traceback (most recent call last):
  File "/app/main.py", line 57, in update_item
    raise ValueError("Invalid input: Negative price not allowed")
ValueError: Invalid input: Negative price not allowed

[2024-11-21 22:27:03] ERROR:    HTTPException: 404 Not Found
Traceback (most recent call last):
  File "/app/main.py", line 72, in get_item
    raise HTTPException(status_code=404, detail="Item not found")
fastapi.exceptions.HTTPException: 404 Not Found

[2024-11-21 22:28:40] ERROR:    pydantic.error_wrappers.ValidationError: 1 validation error for Item
name
  field required (type=value_error.missing)
"""


async def main() -> None:

    llm_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    log_reader = AssistantAgent(
        "log_reader",
        model_client=llm_client,
        description="Log reader",
        system_message=log_reader_system_prompt,
    )

    response = await log_reader.on_messages(
        [TextMessage(content=error_msg, source="user")],
        cancellation_token=CancellationToken(),
    )
    print(response.chat_message.content)


asyncio.run(main())
