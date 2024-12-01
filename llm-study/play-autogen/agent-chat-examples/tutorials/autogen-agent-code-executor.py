import asyncio
import os

from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage  # Add this import
from autogen_core.base import CancellationToken


async def run_code_executor_agent() -> None:
    # Create a code executor agent that uses a Docker container to execute code.
    code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
    await code_executor.start()
    code_executor_agent = CodeExecutorAgent("code_executor", code_executor=code_executor)

    # Run the agent with a given code snippet.
    task = TextMessage(
        content="""Here is some code
```python
print('Hello world')
```
""",
        source="user",
    )
    response = await code_executor_agent.on_messages([task], CancellationToken())
    print(response.chat_message)

    # Stop the code executor.
    await code_executor.stop()

asyncio.run(run_code_executor_agent())
