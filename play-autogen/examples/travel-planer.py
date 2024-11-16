# Travel Planning
# https://microsoft.github.io/autogen/0.4.0.dev6/user-guide/agentchat-user-guide/examples/travel-planning.html

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models import OpenAIChatCompletionClient
from autogen_agentchat.task import Console


async def run_travel_planner() -> None:

    llm_client=OpenAIChatCompletionClient(model="gpt-4o-mini")

    planner_agent = AssistantAgent(
    "planner_agent",
    model_client=llm_client,
    description="A helpful assistant that can plan trips.",
    system_message='''
    You are a helpful assistant that can suggest a travel plan for a user based on their request
    ''',
    )

    local_agent = AssistantAgent(
        "local_agent",
        model_client=llm_client,
        description="A local assistant that can suggest local activities or places to visit.",
        system_message='''
        You are a helpful assistant that can suggest authentic and interesting local 
        activities or places to visit for a user and can utilize any context information provided.
        ''',
    )

    language_agent = AssistantAgent(
        "language_agent",
        model_client=llm_client,
        description="A helpful assistant that can provide language tips for a given destination.",
        system_message='''
        You are a helpful assistant that can review travel plans, providing feedback on important/critical tips 
        about how best to address language or communication challenges for the given destination. 
        If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.
        ''',
    )

    travel_summary_agent = AssistantAgent(
        "travel_summary_agent",
        model_client=llm_client,
        description="A helpful assistant that can summarize the travel plan.",
        system_message='''
        You are a helpful assistant that can take in all of the suggestions and advice from the other agents and 
        provide a detailed tfinal travel plan. You must ensure th b at the final plan is integrated and complete. 
        YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, 
        you can respond with TERMINATE.
        ''',
    )

    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        [planner_agent, local_agent, language_agent, travel_summary_agent], termination_condition=termination
    )

    # Stream the messages to the console.
    await Console(group_chat.run_stream(task="Plan a 3 day trip to Nepal."))

asyncio.run(run_travel_planner())