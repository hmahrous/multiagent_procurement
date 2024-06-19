from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv, load_dotenv
from utils import *
from prompts import system_prompts
from langchain.schema import StrOutputParser
from tools import *

load_dotenv(find_dotenv())

class AgentMain:
    def __init__(self, agent):
        self.agent = agent

    def receive_message(self, message):
        print(f'input: {message}')
        if isinstance(message, list):
            response = self.agent.invoke({"messages": message})
        else:
            response = self.agent.invoke({"messages": [message]})
        try:
            answer = response["output"]
        except:
            answer = response
        print(f'output: {answer}')
        return answer

class AgentFactory:
    def __init__(self, llm):
        self.llm = llm

    def create_conversation_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompts["Conversation-Agent"]),
            MessagesPlaceholder(variable_name="messages"),
        ])
        agent_notetaker = prompt | self.llm | StrOutputParser()
        return AgentMain(agent_notetaker)

    def create_procurement_specialist_agent(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompts["Procurement-Specialist-Agent"]),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(self.llm, [knowledge_base_tool], prompt)
        agent_executor = AgentExecutor(agent=agent, tools=[knowledge_base_tool], verbose=True)
        return AgentMain(agent_executor)

    def create_note_take_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompts["Note-Take-Agent"]),
            MessagesPlaceholder(variable_name="messages"),
        ])
        agent_notetaker = prompt | self.llm | StrOutputParser()
        return AgentMain(agent_notetaker)

    def create_guardrails_agent(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompts["Guardrails-Agent"]),
            MessagesPlaceholder(variable_name="messages"),
        ])
        agent_guardrails = prompt | self.llm | StrOutputParser()
        return AgentMain(agent_guardrails)

def initialize_agents():
    llm = ChatOpenAI(model="gpt-4o")
    factory = AgentFactory(llm)
    agents = {
        "Conversation-Agent": factory.create_conversation_agent(),
        "Procurement-Specialist-Agent": factory.create_procurement_specialist_agent(),
        "Note-Take-Agent": factory.create_note_take_agent(),
        "Guardrails-Agent": factory.create_guardrails_agent(),
    }
    return agents

agents = initialize_agents()
