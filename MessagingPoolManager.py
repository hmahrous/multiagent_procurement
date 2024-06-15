from typing import List, Dict, Any

class MessagingPoolManager:
    def __init__(self):
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}

    def add_message(self, message: Dict[str, Any]):
        self.pool.append(message)

    def subscribe(self, agent_name: str, topics: List[str]):
        self.subscriptions[agent_name] = topics

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        topics = self.subscriptions.get(agent_name, [])
        messages = [msg for msg in self.pool if msg['type'] in topics or msg['from'] in topics]
        return messages