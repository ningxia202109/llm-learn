import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.task import Console


# Create an OpenAI model client.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
)

# Create the primary agent.
primary_agent = AssistantAgent(
    "primary",
    model_client=model_client,
    system_message="You are a helpful AI assistant.",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "critic",
    model_client=model_client,
    system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
)

# Define a termination condition that stops the task if the critic approves.
text_termination = TextMentionTermination("APPROVE")
# Define a termination condition that stops the task after 5 messages.
max_message_termination = MaxMessageTermination(5)
# Combine the termination conditions using the `|`` operator so that the
# task stops when either condition is met.
termination = text_termination | max_message_termination

# Create a team with the primary and critic agents.
reflection_team = RoundRobinGroupChat(
    [primary_agent, critic_agent], termination_condition=termination
)

async def main():
    # Run the first task
    await Console(reflection_team.run_stream(task="Write a short poem about fall season."))
    
    # Run the second task
    await Console(reflection_team.run_stream(task="用中文唐诗风格写诗。"))

    await Console(reflection_team.run_stream())

# Run the main coroutine
asyncio.run(main())
