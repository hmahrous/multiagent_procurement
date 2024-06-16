from typing import List, Dict, Any

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
        print(f"Message added to pool: {message}")

    def subscribe(self, agent_name: str, senders: List[str]):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        senders = self.subscriptions.get(agent_name, [])
        messages = [
            msg for msg in self.pool
            if msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]
        ]
        print(f"{agent_name} has {len(messages)} messages to process.")
        return messages

    def mark_as_processed(self, agent_name: str, message_id: str):
        self.processed_messages[agent_name].append(message_id)
        print(f"Message {message_id} marked as processed by {agent_name}")

    def get_next_msg_id(self):
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    def process_messages(self):
        for agent_name in self.subscriptions:
            messages = self.get_messages(agent_name)
            for message in messages:
                print(f"Processing message {message['id']} for {agent_name}")
                self.send_message(agent_name, message)
                self.mark_as_processed(agent_name, message['id'])

    def send_message(self, agent_name: str, message: Dict[str, Any]):
        agent = self.get_agent_by_name(agent_name)
        if agent:
            agent.receive_message(message)

    def get_agent_by_name(self, agent_name: str):
        return next((agent for agent in self.agents if agent.name == agent_name), None)
