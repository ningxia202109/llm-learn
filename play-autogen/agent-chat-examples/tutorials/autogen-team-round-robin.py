import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.base import TaskResult
from autogen_agentchat.task import Console


# Create an OpenAI model client.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    # api_key="sk-...", # Optional if you have an OPENAI_API_KEY env variable set.
)


# Define a tool that gets the weather for a city.
async def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is 72 degrees and Sunny."


# Create an assistant agent.
weather_agent = AssistantAgent(
    "assistant",
    model_client=model_client,
    tools=[get_weather],
    system_message="Respond 'TERMINATE' when task is complete.",
)

# Define a termination condition.
text_termination = TextMentionTermination("TERMINATE")

# Create a single-agent team.
single_agent_team = RoundRobinGroupChat([weather_agent], termination_condition=text_termination)


async def run_team() -> None:
    result = await single_agent_team.run(task="What is the weather in New York?")
    print(result)


# asyncio.run(run_team())

# asyncio.run(single_agent_team.reset())

async def run_team_stream() -> None:
    async for message in single_agent_team.run_stream(task="What is the weather in New York?"):
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message)

# asyncio.run(run_team_stream())

async def run_team_on_console() -> None:
    # Stream the messages to the console.
    await Console(single_agent_team.run_stream(task="What is the weather in Seattle?"))  

asyncio.run(run_team_on_console())

