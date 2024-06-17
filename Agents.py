from typing import List, Dict, Any, Annotated
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from State import initial_state
import chainlit as cl
from langchain.vectorstores.faiss import FAISS
from dotenv import find_dotenv, load_dotenv
from utils import *
from prompts import system_prompts
from langchain.schema import StrOutputParser
from tools import*

load_dotenv(find_dotenv())

class AgentMain:
    def __init__(self, agent):
        self.agent = agent

    def receive_message(self, message):
        # Handle received message
        response = self.agent.invoke({"messages": [message]})
        try:
            answer = response["output"]
        except:
            answer = response
        return answer



agents = {}
llm = ChatOpenAI(model="gpt-4o")

#create convaersationagent
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompts["Conversation-Agent"]),
    MessagesPlaceholder(variable_name="messages"),])
# Create the chain
agent_notetaker = prompt | llm | StrOutputParser()
agents["Conversation-Agent"] = AgentMain(agent_notetaker)



# Create the agent using the prompt and the tool
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompts["Procurement-Specialist-Agent"],
        ),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
agent = create_openai_functions_agent(llm, [knowledge_base_tool], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[knowledge_base_tool], verbose=True)
agents["Procurement-Specialist-Agent"] = AgentMain(agent_executor)


#create note taker-agent
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompts["Note-Take-Agent"]),
    MessagesPlaceholder(variable_name="messages"),])
# Create the chain
agent_notetaker = prompt | llm | StrOutputParser()
agents["Note-Take-Agent"] = AgentMain(agent_notetaker)



#create guardrails-Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompts["Guardrails-Agent"]),
    MessagesPlaceholder(variable_name="messages"),])
# Create the chain
agent_guardrails= prompt | llm | StrOutputParser()
agents["Guardrails-Agent"] = AgentMain(agent_guardrails)








# # Create agents

# for role in roles:
#     system_prompt = system_prompts[role]
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", system_prompt),
#             MessagesPlaceholder(variable_name="messages"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )
#     if role == "Procurement-Specialist-Agent":
#         tools = [knowledge_base_tool]
#     agent = create_openai_functions_agent(llm, tools, prompt)
#     agent_e = AgentExecutor(agent=agent, tools=tools)
#     agents[role] = AgentMain(agent_e)
#     tools = [dummy_tool]

