import State as state
from MessagingPoolManager import MessagingPoolManager

class DummyAgent:
    def __init__(self, name: str, pool_manager: MessagingPoolManager):
        self.name = name
        self.pool_manager = pool_manager
        self.pool_manager.subscribe(self.name, self.get_subscription_list())
        self.state = state.initial_state

    def get_subscription_list(self):
        if self.name == "Note-Take-Agent":
            return ["user", "Procurement-Specialist-Agent"]
        elif self.name == "Procurement-Specialist-Agent":
            return ["Note-Take-Agent", "Conversation-Agent"]
        elif self.name == "Conversation-Agent":
            return ["user", "Procurement-Specialist-Agent", "Guardrails-Agent"]
        elif self.name == "Guardrails-Agent":
            return ["user", "Conversation-Agent"]
        else:
            return []

    def process_messages(self):
        messages = self.pool_manager.get_messages(self.name)
        for msg in messages:
            print(f"{self.name} received message: {msg}")
            if msg['type'] == 'query' and self.name == "Conversation-Agent":
                self.pool_manager.add_message({"type": "query", "content": msg['content'], "from": "Conversation-Agent"})
            elif msg['type'] == 'instruction' and self.name == "Note-Take-Agent":
                template = {"num_laptops": "", "last_change": "", "ram_requirements": "", "os": "", "project_based": ""}
                self.pool_manager.add_message({"type": "state_update", "content": {"required_info_template": template}, "from": "Note-Take-Agent"})
            elif msg['type'] == 'response' and self.name == "Note-Take-Agent":
                self.state['captured_info'] = msg['content']
                self.pool_manager.add_message({"type": "state_update", "content": {"captured_info": msg['content']}, "from": "Note-Take-Agent"})
            elif msg['type'] == 'state_update' and self.name == "Guardrails-Agent":
                self.pool_manager.add_message({"type": "validation", "content": "User request within guidelines.", "from": "Guardrails-Agent"})
            elif msg['type'] == 'validation' and self.name == "Conversation-Agent":
                self.pool_manager.add_message({"type": "completion", "content": "All required information gathered.", "from": "Conversation-Agent"})