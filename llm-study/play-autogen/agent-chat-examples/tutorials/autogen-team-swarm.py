import asyncio
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.task import MaxMessageTermination


async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    agent1 = AssistantAgent(
        "Alice",
        model_client=model_client,
        handoffs=["Bob"],
        system_message="You are Alice and you only answer questions about yourself.",
    )
    agent2 = AssistantAgent(
        "Bob", model_client=model_client, system_message="You are Bob and your birthday is on 1st January."
    )

    termination = MaxMessageTermination(3)
    team = Swarm([agent1, agent2], termination_condition=termination)

    stream = team.run_stream(task="What is bob's birthday?")
    async for message in stream:
        print(message)


asyncio.run(main())