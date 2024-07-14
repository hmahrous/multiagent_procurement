import asyncio
import json
import logging

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from src.core.config import get_settings
from src.models.state import initial_state
from src.services.prompt_service import SystemPrompts
from src.services.tool_service import tool_runner #, knowledge_base_tool_

logging.basicConfig(level=logging.INFO)
#tool_runnable = knowledge_base_tool_()

class AgentMain:
    def __init__(self, name, agent, prompt_formatter=None):
        self.name = name
        self.agent = agent
        self.prompt_formatter = prompt_formatter

    async def receive_message(self, messages):
        if not messages:
            return ""

        if isinstance(messages, dict):
            messages = [messages]
        elif isinstance(messages, str):
            try:
                messages = json.loads(messages)
                if isinstance(messages, dict):
                    messages = [messages]
            except json.JSONDecodeError:
                raise ValueError(
                    "Invalid message format: expected a list of dictionaries or a JSON string."
                )

        for message in messages:
            if (
                not isinstance(message, dict)
                or "from" not in message
                or "content" not in message
            ):
                raise ValueError(
                    "Each message must be a dictionary with 'from' and 'content' keys."
                )

        common_content = {
            "from": (" & ").join([message["from"] for message in messages]),
            "role": "assistant",
            "content": (
                self.prompt_formatter(messages)
                if self.prompt_formatter
                else "\n".join(
                    [f'{message["from"]}:{message["content"]}' for message in messages]
                )
            ),
        }

        # Ensure the input includes all expected keys
        input_data = {"messages": [common_content]}
        logging.info(f"Input to {self.name} : {input_data}")
        response = await self.agent.ainvoke(input_data)
        try:
            answer = response["output"]
        except Exception:
            answer = response
        logging.info(f"Response from {self.name}: {answer}")
        return answer


class AgentFactory:
    def __init__(self, llm):
        self.llm = llm
        self.system_prompts = {
            "Conversation-Agent": SystemPrompts.CONVERSATION_AGENT,
            "Procurement-Specialist-Agent": SystemPrompts.PROCUREMENT_SPECIALIST_AGENT,
            "Note-Take-Agent": SystemPrompts.NOTE_TAKE_AGENT,
            "Guardrails-Agent": SystemPrompts.GUARDRAILS_AGENT,
        }

    def create_conversation_agent(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompts["Conversation-Agent"]),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agent_notetaker = prompt | self.llm | StrOutputParser()
        return AgentMain("Conversation-Agent", agent_notetaker, prompt_formatter=None)

    def create_procurement_specialist_agent(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompts["Procurement-Specialist-Agent"]),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(self.llm, [tool_runner], prompt)
        agent_procurement = AgentExecutor(
            agent=agent, tools=[tool_runner], verbose=True
        )
        return AgentMain(
            "Procurement-Specialist-Agent", agent_procurement, prompt_formatter=None
        )

    def create_note_take_agent(self):
        def _note_taking_prompt_formatter(messages):
            formatted_message = (
                f'continue from history conversations: ...{str(initial_state["messages"][-3:])} \n'
                + f'Fill this schema (and only this schema) from the user message if relevant:\n {initial_state["captured_info"]}. \n current message:'
                + "\n".join(
                    [f'{message["from"]}:{message["content"]}' for message in messages]
                )
            )
            return formatted_message

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompts["Note-Take-Agent"]),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agent_notetaker = prompt | self.llm | JsonOutputParser()
        return AgentMain("Note-Take-Agent", agent_notetaker, prompt_formatter=None)

    def create_guardrails_agent(self):
        def _guardrails_prompt_formatter(messages):
            formatted_message = "\n".join(
                [f'{message["from"]}:{message["content"]}' for message in messages]
            )
            return formatted_message

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompts["Guardrails-Agent"]),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        agent_guardrails = prompt | self.llm | StrOutputParser()
        return AgentMain("Guardrails-Agent", agent_guardrails, prompt_formatter=None)


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
