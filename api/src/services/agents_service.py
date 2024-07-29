import asyncio
import json
import logging
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.schema import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.services.prompt_service import SystemPrompts
from src.services.tool_service import tool_runner as fiass_tool_runner
from src.services.model_service import get_llm_model

logging.basicConfig(level=logging.INFO)

class AgentMain:
    def __init__(self, name, agent, prompt_formatter=None):
        self.name = name
        self.agent = agent
        self.prompt_formatter = prompt_formatter

    async def receive_message(self, messages):
        if not messages:
            return ""

        messages = self._process_messages(messages)

        common_content = {
            "from": " & ".join(message["from"] for message in messages),
            "role": "assistant",
            "content": self._format_content(messages),
        }

        input_data = {"messages": [common_content]}
        logging.info(f"Message to {self.name} : {input_data}")

        response = await self.agent.ainvoke(input_data)
        try:
            answer = response.get("output", response)
        except:
            answer = response

        logging.info(f"Response from {self.name}: {answer}")
        return answer

    def _process_messages(self, messages):
        if isinstance(messages, dict):
            messages = [messages]
        elif isinstance(messages, str):
            messages = self._parse_json_messages(messages)

        for message in messages:
            if not isinstance(message, dict) or "from" not in message or "content" not in message:
                raise ValueError("Each message must be a dictionary with 'from' and 'content' keys.")

        return messages

    def _parse_json_messages(self, messages):
        try:
            messages = json.loads(messages)
            if isinstance(messages, dict):
                messages = [messages]
            return messages
        except json.JSONDecodeError:
            raise ValueError("Invalid message format: expected a list of dictionaries or a JSON string.")

    def _format_content(self, messages):
        if self.prompt_formatter:
            return self.prompt_formatter(messages)
        else:
            return "\n".join(f'{message["from"]}:{message["content"]}' for message in messages)

class AgentFactory:
    def __init__(self):
        self.agents = {}

    def get_agents(self):
        return self.agents

    def add_agent(self, agent_name, llm, system_prompt, output='str', tool=None):
        if agent_name not in self.agents:
            self.agents[agent_name] = self._create_agent(agent_name, llm, system_prompt, output, tool)

    def _create_agent(self, agent_name, llm, system_prompt, output='str', tool_runner=None):
        if tool_runner is None:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )
            output_parser = JsonOutputParser if output == 'json' else StrOutputParser
            agent_executor = prompt | llm | output_parser()
        else:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="messages"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            )
            agent = create_openai_functions_agent(llm, [tool_runner], prompt)
            agent_executor = AgentExecutor(agent=agent, tools=[tool_runner], verbose=True)
        return AgentMain(agent_name, agent_executor)

def initialize_agents():
    agents_factory = AgentFactory()
    llm = get_llm_model()
    agents_factory.add_agent("Finance-Agent", llm, SystemPrompts.FINANCE_AGENT)
    agents_factory.add_agent("Medical-Agent", llm, SystemPrompts.MEDICAL_AGENT)
    agents_factory.add_agent("Procurement-Specialist-Agent", llm, SystemPrompts.PROCUREMENT_SPECIALIST_AGENT, tool=fiass_tool_runner)
    agents_factory.add_agent("Note-Take-Agent", llm, SystemPrompts.NOTE_TAKE_AGENT, output='json')
    agents_factory.add_agent("Guardrails-Agent", llm, SystemPrompts.GUARDRAILS_AGENT)
    return agents_factory.get_agents()