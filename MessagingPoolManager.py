from typing import List, Dict, Any, Annotated
import chainlit as cl
from Agents import agents
import json
from State import initial_state


class MessagingPoolManager:
    def __init__(self, agents):
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}
        self.processed_messages: Dict[str, List[str]] = {}
        self.msg_id_counter = 1
        self.agents = agents

    def add_message(self, message: Dict[str, Any]):
        message['id'] = self.get_next_msg_id()
        self.pool.append(message)
        #print(f"Message added to pool: {message}")

    def subscribe(self, agent_name: str, senders: List[str]):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        senders = self.subscriptions.get(agent_name, [])
        messages = [
            msg for msg in self.pool
            if msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]
        ]
        #print(f"{agent_name} has {len(messages)} messages to process.")
        return messages

    def mark_as_processed(self, agent_name: str, message_id: str):
        self.processed_messages[agent_name].append(message_id)
        # print(f"Message {message_id} marked as processed by {agent_name}")
        # print(f'processed messages are: {self.processed_messages}')

    def get_next_msg_id(self):
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    async def process_messages(self):
        while True:
            if not self.pool:
                await self.prompt_user_input()
            else:
                for agent_name in self.subscriptions:
                    messages = self.get_messages(agent_name)
                    for message in messages:
                        self.mark_as_processed(agent_name, message['id'])
                    print(f"unprocessed messages for agent are: {messages}")
                    message_contents = {"from": (" & ").join([message["from"] for message in messages]), 
                                        "content": ("\n").join([f'{message["from"]}:{message["content"]}' for message in messages]),
                                        "role": "assistant"}
                    await self.send_message(agent_name, message_contents)

    async def send_message(self, agent_name: str, message: Dict[str, Any]):
        agent = self.get_agent_by_name(agent_name)
        print(f"agent called is {agent}")
        if agent:
            initial_state["current_speaker"] = agent_name
            #print(message)
            response = agent.receive_message(message)
            if response:
                formatted_response = self.format_response(agent_name, response)
                if agent_name=="Note-Take-Agent":
                    if formatted_response["type"] == "template":
                        initial_state["required_info_template"] = formatted_response["content"]
                    if formatted_response["type"] == "state_update":
                        initial_state["captured_info"] = formatted_response["content"]
                if agent_name=="Conversation-Agent":
                    if formatted_response["to"] == "user":
                        initial_state["query_fulfilled"] = True

                # print(f"formatted response is {formatted_response}")
                # print(type(formatted_response))
                await cl.Message(f'{agent_name}:{formatted_response["content"]}').send()
                self.add_message(formatted_response)
                if formatted_response.get('to') == 'user':
                    await self.prompt_user_input(formatted_response)

    def format_response(self, role, response):
        if isinstance(response, dict):
            return response
        else:
            try:
                response = json.loads(response)
                try:
                    response = json.loads(response["content"])
                    return response
                except:
                    return response
            except:
                if role == "Conversation-Agent":
                    return  {
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

    async def prompt_user_input(self, message: Dict[str, Any] = None):
        initial_state["current_speaker"] = "user"
        # if message:
        #     await cl.Message(content=message['content'], author=message['from']).send()
        user_input = await cl.AskUserMessage(content=f"{message['content']}").send()  # Use Chainlit's input method
        user_input = user_input["output"]
        #print(f"user input is  {user_input}")
        await self.add_user_message(user_input)

    async def add_user_message(self, content: str):
        message = {
            "content": content,
            "from": "user",
            "role": "user",
            "to": "Conversation-Agent"
        }
        initial_state["user_query"] = content
        self.add_message(message)
        await self.process_messages()

    def get_agent_by_name(self, agent_name: str):
        return self.agents.get(agent_name, None)


pool_manager = MessagingPoolManager(agents)
print(f"agents are: {agents}")
# Subscribe agents to specific senders
pool_manager.subscribe("Conversation-Agent", ["user", "Guardrails-Agent", "Procurement-Specialist-Agent"])
pool_manager.subscribe("Procurement-Specialist-Agent", ["Conversation-Agent"])
pool_manager.subscribe("Note-Take-Agent", ["user", "Procurement-Specialist-Agent"])
pool_manager.subscribe("Guardrails-Agent", ["Conversation-Agent", "user"])


# class MessagingPoolManager:
#     def __init__(self):
#         self.pool: List[Dict[str, Any]] = []
#         self.subscriptions: Dict[str, List[str]] = {}

#     def add_message(self, message: Dict[str, Any]):
#         self.pool.append(message)

#     def subscribe(self, agent_name: str, topics: List[str]):
#         self.subscriptions[agent_name] = topics

#     def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
#         topics = self.subscriptions.get(agent_name, [])
#         messages = [msg for msg in self.pool if msg['from'] in topics]
#         return messages
    