import json
import logging
from typing import Any, Dict, List
import asyncio
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.services.model_service import get_llm_model
from src.models.state import initial_state
import copy

lock = asyncio.Lock()

logging.basicConfig(level=logging.INFO)


class MessagingPoolManager:
    def __init__(self, agents):
        self.pool: List[Dict[str, Any]] = []
        self.processed_messages: Dict[str, List[str]] = {}
        self.msg_id_counter = 1
        self.agents = agents
        self.initial_state = copy.deepcopy(initial_state)

    async def process_messages(self, mode="group"):
        results = []
        while True:
            if not self.pool:
                return results
            # get user message
            user_message = self.pool[-1]
            # pass to guardrails agent
            guardrail_response = await self._send_message("Guardrails-Agent", user_message)
            if 'invalid' in guardrail_response['content'].lower():
                results.append(guardrail_response)
                return [results, self.initial_state] if mode == 'group' else [guardrail_response, self.initial_state]
            # pass message to other agents in the pool
            other_agents = [agent for agent in self.agents if agent != "Guardrails-Agent"]
            # Prepare the messages and invoke the agents.
            tasks = [self._handle_messages(agent_name, user_message) for agent_name in other_agents]
            # Run the agents tasks concurrently
            results = await asyncio.gather(*tasks)
            # update state of the query
            self.initial_state["query_fulfilled"] = True
            # Get the participants messages of the query
            relevant_results = [
                res for res in results
                if isinstance(res, dict) and res['from'] != 'Note-Take-Agent' and 'notarelevantquery' not in res[
                    'content'].lower()
            ]
            # if more than one agent responded to the user
            if len(relevant_results) > 1:
                # consolidate the answer and return to the user
                response_to_user = self._consolidate_responses(relevant_results)
            else:
                response_to_user = relevant_results[0]['content'] if relevant_results else 'No relevant response'
            return [results, self.initial_state] if mode == 'group' else [response_to_user, self.initial_state]

    async def add_user_message(self, content: str):
        message = {
            "content": content,
            "from": "user",
            "role": "user",
        }
        self.initial_state["user_query"] = content
        self.initial_state["messages"].append(message)
        self._add_message(message)

    def _add_message(self, message: Dict[str, Any]):
        # create a message id
        message['id'] = self._get_next_msg_id()
        # add the message to the pool
        self.pool.append(message)
        # logging.info(f"Added message to pool: {message}")

    def _consolidate_responses(self, responses: list):
        consolidate_prompt = f"""Given the list of responses by several agents, consolidate their responses into one final message for the reader.
        responses:
        {responses}
            """
        llm = get_llm_model()
        prompt = ChatPromptTemplate.from_messages([
            ("system", 'You are a helpful AI assistant great at summarization'),
            MessagesPlaceholder(variable_name="messages"),
        ])
        # Create the chain
        chain = prompt | llm | StrOutputParser()
        messages = [
            {"role": "user", "content": consolidate_prompt}
        ]
        return chain.invoke(messages)

    def _get_next_msg_id(self):
        # create a message id
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    def _get_agent_messages(self, agent_name):
        if not self.initial_state["messages"]:
            return []
        filtered_messages = []
        for message in self.initial_state["messages"]:
            from_part = message.get("from")
            if from_part == 'user' or from_part == agent_name:
                filtered_messages.append(message)
        return filtered_messages[-5:]

    async def _handle_messages(self, agent_name, messages):
        message_contents = self._prepare_message_contents(agent_name, messages)
        response_dict = await self._send_message(agent_name, message_contents)
        async with lock:
            self.initial_state["messages"].append(response_dict)
        return response_dict

    def _prepare_message_contents(self, agent_name, messages):
        if isinstance(messages, dict):
            messages = [messages]
        common_content = {
            "from": (" & ").join([message["from"] for message in messages]),
            "role": "assistant"
        }
        if agent_name == "Note-Take-Agent":
            common_content[
                "content"] = f'continue from history conversations: ...{str(self._get_agent_messages(agent_name))} \n' + \
                             f'previously captured json: {self.initial_state["captured_info"]} \n please only update and return full json. \n current message:' + \
                             "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
        elif agent_name == "Guardrails-Agent":
            common_content["content"] = "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
        else:
            common_content[
                "content"] = f'continue from history conversations: ...{str(self._get_agent_messages(agent_name))} \n previously captured_info {self.initial_state["captured_info"]} \n current query:' + \
                             "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
        return common_content

    async def _send_message(self, agent_name: str, message: Dict[str, Any]):
        agent = self._get_agent_by_name(agent_name)
        if agent:
            self.initial_state["current_speaker"] = agent_name
            response = await agent.receive_message(message)  # Ensure await here
            if response:
                formatted_response = self._format_response(agent_name, response)
                logging.info(f"Formatted response from {agent_name}: {formatted_response}")
                await self._handle_agent_response(agent_name, formatted_response)  # Ensure await here
                return formatted_response

    def _format_response(self, role, response):
        if isinstance(response, dict):
            return response
        try:
            response = json.loads(response)
            try:
                response = json.loads(response["content"])
                return response
            except:
                return response
        except:
            return self._get_default_response_format(role, response)

    def _get_default_response_format(self, role, response):
        if role == "Note-Take-Agent":
            return {
                "type": "template",
                "content": response,
                "from": "Note-Take-Agent",
                "role": "assistant",
            }
        elif role == "Guardrails-Agent":
            return {
                "type": "validation",
                "content": response,
                "from": "Guardrails-Agent",
                "role": "assistant"
            }
        else:
            return {
                "type": "query",
                "content": response,
                "from": role,
                "role": "assistant"
            }

    async def _handle_agent_response(self, agent_name: str, formatted_response: Dict[str, Any]):
        """
        Handle the response from the agent, send it back to the user if necessary,
        and add it to the message pool.
        """
        if not isinstance(formatted_response, dict):
            logging.error(f"Expected formatted_response to be a dict, got {type(formatted_response)} instead.")
            formatted_response = self._get_default_response_format(agent_name, formatted_response)

        if agent_name == "Note-Take-Agent":
            if formatted_response["type"] == "template":
                self.initial_state["required_info_template"] = formatted_response["content"]
            if formatted_response["type"] == "state_update":
                self.initial_state["captured_info"] = formatted_response["content"]
        self._add_message(formatted_response)

    def _get_agent_by_name(self, agent_name: str):
        return self.agents.get(agent_name, None)

