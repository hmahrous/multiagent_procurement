import json
import logging
from typing import Any, Dict, List
from src.models.state import initial_state

#logging.basicConfig(level=logging.INFO)

class MessagingPoolManager:
    def __init__(self, agents):
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}
        self.processed_messages: Dict[str, List[str]] = {}
        self.msg_id_counter = 1
        self.agents = agents
        self._initialize_subscriptions()

    def _initialize_subscriptions(self):
        # Subscribe agents to specific senders
        self.subscribe("Conversation-Agent", ["user", "Procurement-Specialist-Agent"])
        self.subscribe("Procurement-Specialist-Agent", ["Conversation-Agent"])
        self.subscribe("Note-Take-Agent", ["user"])
        self.subscribe("Guardrails-Agent", ["user"])

    def add_message(self, message: Dict[str, Any]):
        message['id'] = self._get_next_msg_id()
        self.pool.append(message)
        #logging.info(f"Added message to pool: {message}")

    def subscribe(self, agent_name: str, senders: List[str]):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        senders = self.subscriptions.get(agent_name, [])
        messages = [msg for msg in self.pool if msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]]
        #logging.info(f"Messages for agent {agent_name}: {messages}")
        return messages

    def mark_as_processed(self, agent_name: str, message_id: str):
        self.processed_messages[agent_name].append(message_id)
        #logging.info(f"Marked message {message_id} as processed for agent {agent_name}")

    def _get_next_msg_id(self):
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    async def process_messages(self, mode="group"):
        results = []
        while True:
            if not self.pool:
                return results  # Return if no messages in the pool
            else:
                for agent_name in self.subscriptions:
                    messages = self.get_messages(agent_name)
                    for message in messages:
                        self.mark_as_processed(agent_name, message['id'])
                    response = await self._handle_messages(agent_name, messages, mode)  # Ensure await here
                    if response:
                        results.append(response)
                        if 'to' in response:
                            if response['to'] == 'user':
                                return results if mode == 'group' else response

    async def _handle_messages(self, agent_name, messages, mode):
        message_contents = self._prepare_message_contents(agent_name, messages)
        response = await self.send_message(agent_name, message_contents)  # Ensure await here
        #logging.info(f"Handled messages for agent {agent_name}: {response}")
        return response

    def _prepare_message_contents(self, agent_name, messages):
        common_content = {
            "from": (" & ").join([message["from"] for message in messages]),
            "role": "assistant"
        }
        if agent_name in ["Conversation-Agent", "Procurement-Specialist-Agent"]:
            common_content[
                "content"] = f'continue from history conversations: ...{str(initial_state["messages"][-5:])} \n previously captured_info {initial_state["captured_info"]} \n current query:' + \
                             "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])

        elif agent_name == "Note-Take-Agent":
            common_content[
                "content"] = f'continue from history conversations: ...{str(initial_state["messages"][-5:])} \n' + \
                             f'previously captured json: {initial_state["captured_info"]} \n please only update and return. \n current message:' + \
                             "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])

        else:
            common_content["content"] = "\n".join([f'{message["from"]}:{message["content"]}' for message in messages])

        #logging.info(f"Prepared message contents for agent {agent_name}: {common_content}")
        return common_content

    async def send_message(self, agent_name: str, message: Dict[str, Any]):
        agent = self._get_agent_by_name(agent_name)
        if agent:
            initial_state["current_speaker"] = agent_name
            response = await agent.receive_message(message)  # Ensure await here
            if response:
                formatted_response = self._format_response(agent_name, response)
                await self._handle_agent_response(agent_name, formatted_response)  # Ensure await here
                #logging.info(f"Sent message to agent {agent_name}, received response: {formatted_response}")
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
        if role == "Conversation-Agent":
            return {
                "type": "query",
                "content": response,
                "from": "Conversation-Agent",
                "role": "assistant",
                "to": "Procurement-Specialist-Agent"
            }
        elif role == "Procurement-Specialist-Agent":
            return {
                "type": "instruction",
                "content": response,
                "from": "Procurement-Specialist-Agent",
                "role": "assistant",
                "to": ["Conversation-Agent", "Note-Take-Agent"]
            }
        elif role == "Note-Take-Agent":
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

    async def _handle_agent_response(self, agent_name: str, formatted_response: Dict[str, Any]):
        """
        Handle the response from the agent, send it back to the user if necessary,
        and add it to the message pool.
        """
        if agent_name == "Note-Take-Agent":
            if formatted_response["type"] == "template":
                initial_state["required_info_template"] = formatted_response["content"]
            if formatted_response["type"] == "state_update":
                initial_state["captured_info"] = formatted_response["content"]
        if agent_name == "Conversation-Agent":
            if formatted_response["to"] == "user":
                initial_state["query_fulfilled"] = True

        self.add_message(formatted_response)

    async def prompt_user_input(self, message: Dict[str, Any] = None):
        initial_state["current_speaker"] = "user"
        user_input = input(f"{message['content']}")
        await self.add_user_message(message['content'], user_input)

    async def add_user_message(self, query: str, content: str):
        message = {
            "content": content,
            "from": "user",
            "role": "user",
            "to": "Conversation-Agent"
        }
        initial_state["user_query"] = content
        initial_state["messages"].append({"you": query, "user": content})
        self.add_message(message)
        #logging.info(f"Added user message: {message}")
        # return await self.process_messages()

    def _get_agent_by_name(self, agent_name: str):
        return self.agents.get(agent_name, None)
