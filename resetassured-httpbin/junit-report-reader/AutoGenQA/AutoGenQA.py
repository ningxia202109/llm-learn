import asyncio

from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core.base import CancellationToken
from autogen_agentchat.agents import AssistantAgent


def _ai_qa_engineer_exp() -> str:
    qa_engineer_prompt = """
You are an experianxe QA engineer, you read error_message and then investgate the root cause of the error based on POSSIBLE_ISSUES, 
and provide solution from POSSIBLE_SOLUTIONS, reply clear and short message in json that follow EXAMPLE_ANSWER.
<POSSIBLE_ISSUES>
- expectation failed of returned http status code
- expectation failed in returned header
- expectation failed in returned body
</POSSIBLE_ISSUES>

<POSSIBLE_SOLUTIONS>
- if expection failed, test script need update or test api has regression issue.
</POSSIBLE_SOLUTIONS>

<EXAMPLE_ANSWER>
{
    "error_message": "",
    "error_field": "",
    "expected_value": "",
    "actual_value": "",
    "solution": ""
}
</EXAMPLE_ANSWER>
"""
    return qa_engineer_prompt


async def _ai_process_error_message(error_message) -> str:

    ai_qa_agent = AssistantAgent(
        name="assistant",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-mini",
        ),
        system_message=_ai_qa_engineer_exp(),
    )

    response = await ai_qa_agent.on_messages(
        [TextMessage(content=error_message, source="error_message")],
        cancellation_token=CancellationToken(),
    )

    return response.chat_message.content


def auto_gen_qa(error_message):
    # Process the error log and get the LLM response
    ai_analysis = asyncio.run(_ai_process_error_message(error_message))

    return ai_analysis
