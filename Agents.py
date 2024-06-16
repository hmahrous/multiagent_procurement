class Agent_MAIN:
    def __init__(self, name):
        self.name = name
        self.manager = None
        self.processed_instructions = set()

    def subscribe_to_manager(self, manager):
        self.manager = manager
        self.manager.subscribe(self.name, self.get_subscribed_types())

    def get_subscribed_types(self):
        return []

    def receive_message(self, message):
        print(f"{self.name} received message: {message}")
        self.process_message(message)

    def process_message(self, message):
        raise NotImplementedError

class ConversationAgentDummy(Agent_MAIN):
    def __init__(self, name):
        super().__init__(name)
        self.questions_asked = False

    def get_subscribed_types(self):
        return ["user", "Guardrails-Agent", "Procurement-Specialist-Agent"]

    def process_message(self, message):
        if message["from"] == "user" and message["type"] == "query" and not self.questions_asked:
            self.manager.add_message({
                "type": "query",
                "content": "I need to figure out what is the required process. Please advise.",
                "from": "Conversation-Agent"
            })
        elif message["from"] == "Procurement-Specialist-Agent" and message["type"] == "instruction":
            if message['content'] not in self.processed_instructions and not self.questions_asked:
                self.manager.add_message({
                    "type": "query",
                    "content": "Could you please provide the number of laptops, when was the last time your team changed laptops, RAM requirements, Operating system, and whether this is for a project or a complete replacement?",
                    "from": "Conversation-Agent"
                })
                self.processed_instructions.add(message['content'])
                self.questions_asked = True
        elif message["from"] == "Guardrails-Agent" and message["type"] == "validation":
            print(f"Guardrails validation: {message['content']}")

class ProcurementSpecialistAgentDummy(Agent_MAIN):
    def get_subscribed_types(self):
        return ["Conversation-Agent"]

    def process_message(self, message):
        if message["type"] == "query":
            if "I need to figure out what is the required process" in message["content"]:
                self.manager.add_message({
                    "type": "instruction",
                    "content": "Please ask for these required key specifications: Is this for a new project or ongoing project? Is this a temporary replacement or permanent replacement? How many laptops are needed? How many GB RAM?",
                    "from": "Procurement-Specialist-Agent"
                })
                self.manager.add_message({
                    "type": "instruction",
                    "content": "Please take note of this initial set of requirements from the user",
                    "from": "Procurement-Specialist-Agent"
                })

class NoteTakerAgentDummy(Agent_MAIN):
    def get_subscribed_types(self):
        return ["user", "Procurement-Specialist-Agent"]

    def process_message(self, message):
        if message["type"] == "instruction" and "Please take note" in message["content"]:
            print(f"NoteTaker-Agent updating state with message: {message}")
            # Here you would update the internal state or database

class GuardrailsAgentDummy(Agent_MAIN):
    def get_subscribed_types(self):
        return ["user"]

    def process_message(self, message):
        if message["type"] == "query":
            self.manager.add_message({
                "type": "validation",
                "content": "User request within guidelines.",
                "from": "Guardrails-Agent"
            })
