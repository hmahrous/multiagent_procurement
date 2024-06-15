from typing import List, Dict, Any


class MessagingPoolManager:
    def __init__(self):
        self.pool: List[Dict[str, Any]] = []
        self.subscriptions: Dict[str, List[str]] = {}
        self.processed_messages: Dict[str, List[str]] = {}

    def add_message(self, message: Dict[str, Any]):
        self.pool.append(message)

    def subscribe(self, agent_name: str, senders: List[str]):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        senders = self.subscriptions.get(agent_name, [])
        messages = [
            msg for msg in self.pool
            if msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]
        ]
        return messages

    def mark_as_processed(self, agent_name: str, message_id: str):
        self.processed_messages[agent_name].append(message_id)


class DummyAgent:
    def __init__(self, name: str, pool_manager: MessagingPoolManager):
        self.name = name
        self.pool_manager = pool_manager
        self.pool_manager.subscribe(self.name, self.get_subscription_list())
        self.state = initial_state.copy()
        self.msg_id_counter = 1

    def get_subscription_list(self):
        if self.name == "Note-Take-Agent":
            return ["Conversation-Agent", "Procurement-Specialist-Agent", "user"]
        elif self.name == "Procurement-Specialist-Agent":
            return ["user"]
        elif self.name == "Conversation-Agent":
            return ["Procurement-Specialist-Agent", "Note-Take-Agent", "Guardrails-Agent", "user"]
        elif self.name == "Guardrails-Agent":
            return ["user"]
        else:
            return []

    def get_next_msg_id(self):
        msg_id = f"msg{self.msg_id_counter}"
        self.msg_id_counter += 1
        return msg_id

    def process_messages(self):
        messages = self.pool_manager.get_messages(self.name)
        for msg in messages:
            print(f"{self.name} received message: {msg}")
            if msg['type'] == 'query' and self.name == "Conversation-Agent":
                self.pool_manager.add_message({
                    "id": self.get_next_msg_id(),
                    "type": "instruction",
                    "content": "Please ask for laptop specifications...",
                    "from": "Conversation-Agent",
                    "to": ["user"]
                })
            elif msg['type'] == 'query' and self.name == "Procurement-Specialist-Agent":
                self.pool_manager.add_message({
                    "id": self.get_next_msg_id(),
                    "type": "instruction",
                    "content": "Please ask for laptop specifications...",
                    "from": "Procurement-Specialist-Agent",
                    "to": ["Conversation-Agent"]
                })
            elif msg['type'] == 'instruction' and self.name == "Note-Take-Agent":
                self.pool_manager.add_message({
                    "id": self.get_next_msg_id(),
                    "type": "instruction",
                    "content": "Please provide the specifications for the laptops needed.",
                    "from": "Note-Take-Agent",
                    "to": ["user"]
                })
            elif msg['type'] == 'response' and self.name == "Note-Take-Agent":
                self.state['captured_info'] = msg['content']
                self.pool_manager.add_message({
                    "id": self.get_next_msg_id(),
                    "type": "completion",
                    "content": "All required information gathered.",
                    "from": "Note-Take-Agent",
                    "to": ["Conversation-Agent"]
                })
            elif msg['type'] == 'completion' and self.name == "Conversation-Agent":
                self.pool_manager.add_message({
                    "id": self.get_next_msg_id(),
                    "type": "completion",
                    "content": "Request complete. All information gathered and validated.",
                    "from": "Conversation-Agent",
                    "to": ["user"]
                })
            elif msg['type'] == 'query' and self.name == "Guardrails-Agent":
                if self.validate_user_request(msg['content']):
                    self.pool_manager.add_message({
                        "id": self.get_next_msg_id(),
                        "type": "validation",
                        "content": "User request within guidelines.",
                        "from": "Guardrails-Agent",
                        "to": ["Conversation-Agent"]
                    })
                else:
                    self.pool_manager.add_message({
                        "id": self.get_next_msg_id(),
                        "type": "validation",
                        "content": "User request not within guidelines. Please review.",
                        "from": "Guardrails-Agent",
                        "to": ["Conversation-Agent"]
                    })

            self.pool_manager.mark_as_processed(self.name, msg['id'])

    def validate_user_request(self, content: str) -> bool:
        # Implement your validation logic here
        return True


if __name__ == "__main__":
    initial_state = {
        "current_speaker": "user",
        "user_query": "",
        "query_fulfilled": False,
        "category": None,
        "sub_category": None,
        "required_info_template": None,
        "captured_info": {},
        "messages": []
    }

    pool_manager = MessagingPoolManager()

    agent1 = DummyAgent("Conversation-Agent", pool_manager)
    agent2 = DummyAgent("Procurement-Specialist-Agent", pool_manager)
    agent3 = DummyAgent("Note-Take-Agent", pool_manager)
    agent4 = DummyAgent("Guardrails-Agent", pool_manager)

    # User initiates request
    pool_manager.add_message(
        {"id": "msg1", "type": "query", "content": "I need to procure laptops for my team.", "from": "user"})

    # Process each agent step-by-step
    agents = [agent1, agent2, agent3, agent4]
    for agent in agents:
        agent.process_messages()

    # Simulate user response
    pool_manager.add_message({"id": "msg3", "type": "response",
                              "content": {"num_laptops": 10, "last_change": "1 year ago", "ram_requirements": "16GB",
                                          "os": "Windows 10", "project_based": False}, "from": "user"})

    for agent in agents:
        agent.process_messages()
