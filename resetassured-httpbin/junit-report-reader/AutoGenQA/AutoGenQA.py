import asyncio

from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core.base import CancellationToken
from autogen_agentchat.agents import AssistantAgent


def _ai_qa_engineer_exp() -> str:
    qa_engineer_prompt = """
You are an experianxe QA engineer, you read error_message and then investgate the root cause of the error based on POSSIBLE_ISSUES, 
and provide solution from POSSIBLE_SOLUTIONS, reply clear and short message in one line that follow EXAMPLE_ANSWER.
<POSSIBLE_ISSUES>
- expectation failed if return value unmatch expected value
</POSSIBLE_ISSUES>

<POSSIBLE_SOLUTIONS>
- if expection failed present, first, test script need update; second test api has regression issue.
</POSSIBLE_SOLUTIONS>

<EXAMPLE_ANSWER>
expectation failed, field "Access-Control-Allow-Origin", Expected: "", Actual: "", solution: test script need update or test api has regression issue
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


if __name__ == "__main__":
    error_message = f"""
    1 expectation failed. Expected header "Access-Control-Allow-Origin" was not "https://httpbin.org", was "*". Headers are: Date=Wed, 27 Nov 2024 01:10:04 GMT Content-Type=application/json Content-Length=557 Connection=keep-alive Server=gunicorn/19.9.0 Access-Control-Allow-Origin=* Access-Control-Allow-Credentials=true
    """
    # Process the error log and get the LLM response
    ai_analysis = asyncio.run(ai_process_error_message(error_message))

    print(ai_analysis)
