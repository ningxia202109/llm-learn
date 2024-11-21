import asyncio
import os
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_core.components.models import UserMessage

async def main() -> None:
    opneai_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )


    result = await opneai_model_client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(result)

asyncio.run(main())
