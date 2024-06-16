from typing import List, Dict, Any, Annotated
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import json
from State import initial_state
from MessagingPoolManager import MessagingPoolManager
import chainlit as cl


@tool
def dummy_tool(
    content: Annotated[str, "content"]
) -> Annotated[str, "output"]:
    """create something."""
    pass

OPENAI_API_KEY="your_api_key"


# Initialize the pool manager
pool_manager = MessagingPoolManager()

# Define global variable for state

# Define the system prompts for each agent
system_prompts = {
    "Conversation-Agent": """You are the Conversation Agent. Your manage the flow of conversation between the Procurement Specialist Agent  and user.  A user need something, you forward to the procurement specialist agent, if the procurement specialist agent needs more information, you need to tell the user to provide the neccessary details. 

Alwas respond in one of the two formats below:
1.
{{
    "type": "query",
    "content": "<your message>",
    "from": "Conversation-Agent",
    "role": "assistant",
    "to": "Procurement-Specialist-Agent"
}}

2.
{{
    "type": "completion",
    "content": "<your message>",
    "from": "Conversation-Agent",
    "role": "assistant"
    "to": "user"}}
""",
    "Procurement-Specialist-Agent": """You are the Procurement Specialist Agent. Your role is to determine the next steps for procurement. Make sure you get required information
Respond in the format:
{{
    "type": "instruction",
    "content": "<your instructions>",
    "from": "Procurement-Specialist-Agent",
    "role": "assistant",
    "to": ["Conversation-Agent", "Note-Take-Agent"]
}}""",
    "Note-Take-Agent": """You are the Note-Take Agent. Your role is to form templates for required information based on the instructions from the Procurement-Specialist-Agent.
If you receive an instruction containing the word 'specifications', respond with an appropriate empty template.
If you receive a user response, capture the information and update the state, then send confirmation to the pool.
Ensure your reply is in one of this required format, nothing else, if no template/captured_info your content should be an empty dict.
Respond in the format:
For template:
{{
    "type": "template",
    "content": <template>,
    "from": "Note-Take-Agent"
    "role": "assistant",
}}
For state update:
{{
    "type": "state_update",
    "content": {{"captured_info": <captured_info>}},
    "from": "Note-Take-Agent",
    "role": "assistant",}}
    """,
    "Guardrails-Agent": """You are the Guardrails Agent. Your role is to only validate user queries for compliance.
Respond with validation status in the format: 
{{
    "type": "validation",
    "content": "<validation_message>",
    "from": "Guardrails-Agent",
    "role": "assistant"
}}"""
}

# Define the roles for each agent
roles = ["Conversation-Agent", "Procurement-Specialist-Agent", "Note-Take-Agent", "Guardrails-Agent"]

# Define the LLM
llm = ChatOpenAI(model="gpt-4-turbo", openai_api_key=OPENAI_API_KEY)

# Define tools (empty for this example)
tools = [dummy_tool]

# Create agents
agents = {}
for role in roles:
    system_prompt = system_prompts[role]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_functions_agent(llm, tools, prompt)
    agents[role] = AgentExecutor(agent=agent, tools=tools)

# Set up subscriptions
pool_manager.subscribe("Conversation-Agent", ["user", "Procurement-Specialist-Agent", "Guardrails-Agent"])
pool_manager.subscribe("Procurement-Specialist-Agent", ["Conversation-Agent"])
pool_manager.subscribe("Note-Take-Agent", ["user", "Procurement-Specialist-Agent"])
pool_manager.subscribe("Guardrails-Agent", ["Conversation-Agent", "user"])

# Example function to run all agents
to_user = False
async def run_agents():
    while True:
        for role, agent_executor in agents.items():
            initial_state["current_speaker"] = role
            messages = pool_manager.get_messages(role)
            if messages:
                to_user = True if messages[-1].get("to", "") == "user" else False
                if to_user:
                    initial_state["query_fulfilled"]=True
                    break
                response = agent_executor.invoke({"messages": messages})
                response = response["output"]
                try:
                    response = json.loads(response)
                except:
                    continue
                pool_manager.add_message(response)
                print(f'{role}:{response["content"]}')
                print()
                await cl.Message(f'{role}:{response["content"]}').send()
                if role=="Note-Take-Agent":
                    if response["type"] == "template":
                        initial_state["required_info_template"] = response["content"]
                    if response["type"] == "state_update":
                        initial_state["captured_info"] = response["content"]
                # if role=="Procurement-Specialist-Agent":
                #     initial_state["category"] = response["category"]
                #     initial_state["subcategory"] = response["subcategory"]
                #print(initial_state)
                #print()
        if to_user:
            print(response)
            return response["content"]
        


        
            # user_reply = input(f'{messages[-1]["content"]}')
            # user_query = {"type": "query", "content": user_reply, "from": "user", "role":"user"}
            # pool_manager.add_message(user_query)
            # initial_state["user_query"] = user_reply
            # initial_state["query_fulfilled"]=False



# # Example usage
# # User sends a query
# user_query = {"type": "query", "content": "I to procure laptops for my team", "from": "user", "role":"user"}
# initial_state["user_query"] = user_query["content"]
# pool_manager.add_message(user_query)

# # Run all agents
# run_agents()







# Prepare input for the agent
# input_data = {
#     "messages": [message],
#     "agent_scratchpad": "",
#     "type": message.get("type", "query")
# }
#response = agent_executor.invoke(input_data)

# message = messages[-1]
# if role == "Note-Take-Agent":
#     if "specifications" in message["content"]:
#         pool_manager.add_message({
#             "type": "template",
#             "content": response["content"],  # This should be dynamically generated based on the instruction content
#             "from": "Note-Take-Agent"
#         })
#     elif message["type"] == "response":
#         captured_info = message["content"]
#         global_state.update(captured_info)
#         pool_manager.add_message({
#             "type": "state_update",
#             "content": {"captured_info": captured_info},
#             "from": "Note-Take-Agent"
#         })
#         # Share updated state with Conversation-Agent and Procurement-Specialist-Agent
#         pool_manager.add_message({
#             "type": "state_update",
#             "content": {"captured_info": captured_info},
#             "from": "Note-Take-Agent",
#             "to": ["Conversation-Agent", "Procurement-Specialist-Agent"]
#         })
# elif role == "Guardrails-Agent":
#     if "off-topic" in response:
#         pool_manager.add_message({
#             "type": "query",
#             "content": "Your query seems off-topic. Please refine your question.",
#             "from": "Conversation-Agent",
#             "to": "user"
#         })
# elif role == "Conversation-Agent":
#     if "captured_info" in global_state and not global_state.get("approval_requested"):
#         pool_manager.add_message({
#             "type": "query",
#             "content": "All required information gathered. Please confirm to proceed.",
#             "from": "Conversation-Agent",
#             "to": "Procurement-Specialist-Agent"
#         })
#         global_state["approval_requested"] = True
#     elif global_state.get("approval_requested") and response["content"].lower() == "confirmed":
#         pool_manager.add_message({
#             "type": "completion",
#             "content": "The procurement process has been successfully completed.",
#             "from": "Conversation-Agent",
#             "to": "user"
#         })
#         global_state["conversation_ended"] = True
# else:
#     pool_manager.add_message()