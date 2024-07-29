import asyncio
import copy
import json
from typing import List, Dict, Any
import logging
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.services.model_service import get_llm_model
from src.models.state import initial_state

lock = asyncio.Lock()
logging.basicConfig(level=logging.INFO)

class MessagingPoolManager:
    def __init__(self, agents: Dict[str, Any]):
        """
        Initialize the MessagingPoolManager with the given agents.

        Args:
            agents (Dict[str, Any]): Dictionary of agent instances.
        """
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}
        self.processed_messages: Dict[str, List[str]] = {}
        self.msg_id_counter = 1
        self.agents = agents
        self.initial_state = copy.deepcopy(initial_state)
        self._initialize_subscriptions()

    async def process_messages(self, mode: str = "group") -> List[Any]:
        """
        Process messages in the pool, coordinating between agents.

        Args:
            mode (str): Mode of processing ('group' or individual).

        Returns:
            List[Any]: Results of the message processing.
        """
        results = []
        while True:
            if not self.pool:
                return results
            # Process Guardrails-Agent messages first
            guardrail_response = await self._handle_messages("Guardrails-Agent")
            if 'invalid' in str(guardrail_response['content']).lower():
                results.append(guardrail_response)
                return [results, self.initial_state] if mode == 'group' else [guardrail_response, self.initial_state]

            # Prepare and run tasks for other agents concurrently
            tasks = [self._handle_messages(agent) for agent in self.agents if agent != "Guardrails-Agent"]
            results = await asyncio.gather(*tasks)

            # Update query state to fulfilled
            self.initial_state["query_fulfilled"] = True

            # Filter relevant results
            relevant_results = [
                res for res in results
                if isinstance(res, dict) and res['from'] != 'Note-Take-Agent' and 'notarelevantquery' not in res[
                    'content'].lower()
            ]

            # Consolidate responses if more than one relevant result is found
            if len(relevant_results) > 1:
                response_to_user = self._consolidate_responses(relevant_results)
            else:
                response_to_user = relevant_results[0]['content'] if relevant_results else 'No relevant response'

            return [results, self.initial_state] if mode == 'group' else [response_to_user, self.initial_state]

    async def add_user_message(self, content: str):
        """
        Add a user's message to the pool and update the initial state.

        Args:
            content (str): Content of the user's message.
        """
        message = {
            "content": content,
            "from": "user",
            "role": "user",
        }
        self.initial_state["user_query"] = content
        self.initial_state["messages"].append(message)
        self._add_message(message)

    def _initialize_subscriptions(self):
        """Initialize agent subscriptions to specific message senders."""
        self._subscribe("Procurement-Specialist-Agent", ["user", "Note-Take-Agent"])
        self._subscribe("Note-Take-Agent", ["user"])
        self._subscribe("Guardrails-Agent", ["user"])
        self._subscribe("Medical-Agent", ["user"])
        self._subscribe("Finance-Agent", ["user"])

    def _subscribe(self, agent_name: str, senders: List[str]):
        """
        Subscribe an agent to specific senders.

        Args:
            agent_name (str): Name of the agent.
            senders (List[str]): List of sender names.
        """
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def _get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve messages for the specified agent.

        Args:
            agent_name (str): Name of the agent.

        Returns:
            List[Dict[str, Any]]: List of messages for the agent.
        """
        senders = self.subscriptions.get(agent_name, [])
        return [msg for msg in self.pool if
                msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]]

    def _mark_as_processed(self, agent_name: str, message_id: str):
        """
        Mark a message as processed by the specified agent.

        Args:
            agent_name (str): Name of the agent.
            message_id (str): ID of the message.
        """
        self.processed_messages[agent_name].append(message_id)

    def _add_message(self, message: Dict[str, Any]):
        """
        Add a new message to the pool.

        Args:
            message (Dict[str, Any]): Message to be added.
        """
        message['id'] = self._get_next_msg_id()
        self.pool.append(message)

    def _consolidate_responses(self, responses: List[Dict[str, Any]]) -> str:
        """
        Consolidate multiple agent responses into one final message.

        Args:
            responses (List[Dict[str, Any]]): List of responses from agents.

        Returns:
            str: Consolidated response.
        """
        consolidate_prompt = f"Given the list of responses by several agents, consolidate their responses into one final message for the reader.\nResponses:\n{responses}"
        llm = get_llm_model()
        prompt = ChatPromptTemplate.from_messages([
            ("system", 'You are a helpful AI assistant great at summarization'),
            MessagesPlaceholder(variable_name="messages"),
        ])
        chain = prompt | llm | StrOutputParser()
        messages = [{"role": "user", "content": consolidate_prompt}]
        return chain.invoke(messages)

    def _get_next_msg_id(self) -> str:
        """
        Generate the next message ID.

        Returns:
            str: Next message ID.
        """
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    def _get_agent_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve the last five messages for the specified agent.

        Args:
            agent_name (str): Name of the agent.

        Returns:
            List[Dict[str, Any]]: List of last five messages for the agent.
        """
        if not self.initial_state["messages"]:
            return []
        return [msg for msg in self.initial_state["messages"] if msg.get("from") in ['user', agent_name]][-5:]

    async def _handle_messages(self, agent_name: str) -> Dict[str, Any]:
        """
        Handle messages for the specified agent.

        Args:
            agent_name (str): Name of the agent.

        Returns:
            Dict[str, Any]: Response from the agent.
        """
        subscribed_messages = self._get_messages(agent_name)
        for message in subscribed_messages:
            self._mark_as_processed(agent_name, message['id'])

        message_contents = self._prepare_message_contents(agent_name, subscribed_messages)
        response_dict = await self._send_message(agent_name, message_contents)

        async with lock:
            self.initial_state["messages"].append(response_dict)
        return response_dict

    def _prepare_message_contents(self, agent_name: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Prepare message contents for the specified agent.

        Args:
            agent_name (str): Name of the agent.
            messages (List[Dict[str, Any]]): List of messages to prepare.

        Returns:
            Dict[str, Any]: Prepared message contents.
        """
        if isinstance(messages, dict):
            messages = [messages]
        common_content = {
            "from": " & ".join([message["from"] for message in messages]),
            "role": "assistant"
        }

        if agent_name == "Note-Take-Agent":
            common_content["content"] = (
                    f'Continue from history conversations: ...{str(self._get_agent_messages(agent_name))}\n'
                    f'Previously captured JSON: {self.initial_state["captured_info"]}\n'
                    'Please only update and return full JSON.\n'
                    'Current message:\n' + "\n".join(
                [f'{message["from"]}:{message["content"]}' for message in messages])
            )
        elif agent_name == "Guardrails-Agent":
            common_content["content"] = "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
        else:
            common_content["content"] = (
                    f'Continue from history conversations: ...{str(self._get_agent_messages(agent_name))}\n'
                    'Current query:\n' + "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])
            )
        return common_content

    async def _send_message(self, agent_name: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a message to the specified agent and handle its response.

        Args:
            agent_name (str): Name of the agent.
            message (Dict[str, Any]): Message to be sent.

        Returns:
            Dict[str, Any]: Formatted response from the agent.
        """
        agent = self._get_agent_by_name(agent_name)
        if agent:
            self.initial_state["current_speaker"] = agent_name
            response = await agent.receive_message(message)
            if response:
                formatted_response = self._format_response(agent_name, response)
                await self._handle_agent_response(agent_name, formatted_response)
                return formatted_response

    def _format_response(self, role: str, response: Any) -> Dict[str, Any]:
        """
        Format the response from the agent.
            Args:
                role (str): Role of the agent.
                response (Any): Response from the agent.

            Returns:
                Dict[str, Any]: Formatted response.
        """
        if isinstance(response, dict):
            return response
        try:
            response = json.loads(response)
            response = json.loads(response.get("from", "{}"))
            return response
        except json.JSONDecodeError:
            return self._get_default_response_format(role, response)

    def _get_default_response_format(self, role: str, response: Any) -> Dict[str, Any]:
        """
        Get the default response format for the specified role.

        Args:
            role (str): Role of the agent.
            response (Any): Response from the agent.

        Returns:
            Dict[str, Any]: Default formatted response.
        """
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
        Handle the agent's response and update the state accordingly.

        Args:
            agent_name (str): Name of the agent.
            formatted_response (Dict[str, Any]): Formatted response from the agent.
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

    def _get_agent_by_name(self, agent_name: str) -> Any:
        """
        Retrieve the agent instance by its name.

        Args:
            agent_name (str): Name of the agent.

        Returns:
            Any: Agent instance.
        """
        return self.agents.get(agent_name, None)