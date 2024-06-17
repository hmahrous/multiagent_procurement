from typing import List, Dict, Any, TypedDict
import json
import operator
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, FunctionMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolInvocation, ToolExecutor
from langgraph.graph import StateGraph, END

load_dotenv()

# Define the state schema
class ProcurementState(TypedDict):
    category: str
    captured_info: Dict[str, Any]
    messages: List[BaseMessage]

# Initialize the OpenAI model
model = ChatOpenAI(temperature=0, streaming=True)

# Define a simple tool executor (placeholder for now)
tools = []  # Define your tools here
tool_executor = ToolExecutor(tools)

# Define the MessagingPoolManager
class MessagingPoolManager:
    def __init__(self, agents):
        self.pool = []
        self.subscriptions = {}
        self.processed_messages = {}
        self.msg_id_counter = 1
        self.agents = agents

    def add_message(self, message):
        message['id'] = self.get_next_msg_id()
        self.pool.append(message)
        print(f"Message added to pool: {message}")

    def subscribe(self, agent_name, senders):
        self.subscriptions[agent_name] = senders
        self.processed_messages[agent_name] = []

    def get_messages(self, agent_name):
        senders = self.subscriptions.get(agent_name, [])
        messages = [msg for msg in self.pool if msg['from'] in senders and msg['id'] not in self.processed_messages[agent_name]]
        print(f"{agent_name} has {len(messages)} messages to process.")
        return messages

    def mark_as_processed(self, agent_name, message_id):
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

    def send_message(self, agent_name, message):
        agent = self.get_agent_by_name(agent_name)
        if agent:
            agent.receive_message(message)

    def get_agent_by_name(self, agent_name):
        return next((agent for agent in self.agents if agent.name == agent_name), None)

# Define the ConversationAgent using OpenAI
class ConversationAgent:
    def __init__(self, name):
        self.name = name
        self.manager = None
        self.model = model

    def subscribe_to_manager(self, manager):
        self.manager = manager
        self.manager.subscribe(self.name, self.get_subscribed_types())

    def get_subscribed_types(self):
        return ["user", "Guardrails-Agent", "Procurement-Specialist-Agent"]

    def receive_message(self, message):
        print(f"{self.name} received message: {message}")
        self.process_message(message)

    def process_message(self, message):
        # Generate a prompt for the model based on the received message
        prompt = self.generate_prompt(message)
        # Invoke the OpenAI model with the generated prompt
        response = self.model.invoke([HumanMessage(content=prompt)])
        # Extract the content from the AIMessage object
        response_content = response.content
        # Add the response to the messaging pool
        self.manager.add_message({
            "type": "response",
            "content": response_content,
            "from": "Conversation-Agent"
        })

    def generate_prompt(self, message):
        if message["from"] == "user":
            return f"You are a Conversation Agent. Your role is to gather necessary information from the user to complete a procurement request. You are communicating with a central messaging pool and subscribed to the following agents: Guardrails-Agent and Procurement-Specialist-Agent. The user has asked: {message['content']}. Please guide the user by asking relevant questions to gather all necessary details."
        elif message["from"] == "Procurement-Specialist-Agent":
            return f"You are a Conversation Agent. Your role is to gather necessary information from the user to complete a procurement request. The Procurement-Specialist-Agent has provided instructions: {message['content']}. Based on these instructions, ask the user the specific details needed to proceed with the procurement. Ensure that you follow up based on the previous user's responses."
        elif message["from"] == "Guardrails-Agent":
            return f"You are a Conversation Agent. Your role is to gather necessary information from the user to complete a procurement request. The Guardrails-Agent has validated the user's request and confirmed it is within guidelines. Continue the conversation to gather all necessary details from the user and avoid repeating the same questions."
        else:
            return "You are a Conversation Agent. Your role is to assist with procurement requests. Please provide instructions or ask clarifying questions to ensure all necessary information is gathered."

# Define the ProcurementSpecialistAgent using OpenAI
class ProcurementSpecialistAgent:
    def __init__(self, name):
        self.name = name
        self.manager = None
        self.model = model

    def subscribe_to_manager(self, manager):
        self.manager = manager
        self.manager.subscribe(self.name, self.get_subscribed_types())

    def get_subscribed_types(self):
        return ["Conversation-Agent"]

    def receive_message(self, message):
        print(f"{self.name} received message: {message}")
        self.process_message(message)

    def process_message(self, message):
        # Generate a prompt for the model based on the received message
        prompt = self.generate_prompt(message)
        # Invoke the OpenAI model with the generated prompt
        response = self.model.invoke([HumanMessage(content=prompt)])
        # Extract the content from the AIMessage object
        response_content = response.content
        # Add the response to the messaging pool
        self.manager.add_message({
            "type": "instruction",
            "content": response_content,
            "from": "Procurement-Specialist-Agent"
        })

    def generate_prompt(self, message):
        return f"You are a Procurement Specialist Agent. Your role is to provide expertise on specific categories and sub-categories and instruct the Conversation-Agent on what information to capture next. The message from the Conversation-Agent is: {message['content']}. Based on this, provide the necessary instructions."

# Define the NoteTakerAgent using OpenAI
class NoteTakerAgent:
    def __init__(self, name):
        self.name = name
        self.manager = None
        self.model = model

    def subscribe_to_manager(self, manager):
        self.manager = manager
        self.manager.subscribe(self.name, self.get_subscribed_types())

    def get_subscribed_types(self):
        return ["Conversation-Agent", "Procurement-Specialist-Agent"]

    def receive_message(self, message):
        print(f"{self.name} received message: {message}")
        self.process_message(message)

    def process_message(self, message):
        # Generate a prompt for the model based on the received message
        prompt = self.generate_prompt(message)
        # Invoke the OpenAI model with the generated prompt
        response = self.model.invoke([HumanMessage(content=prompt)])
        # Extract the content from the AIMessage object
        response_content = response.content
        # Add the response to the messaging pool
        self.manager.add_message({
            "type": "state_update",
            "content": response_content,
            "from": "NoteTaker-Agent"
        })

    def generate_prompt(self, message):
        return f"You are a NoteTaker Agent. Your role is to capture and record the required information based on the guidelines provided by the Procurement-Specialist-Agent. The message to be recorded is: {message['content']}. Capture the necessary details and update the state."

# Define the GuardrailsAgent using OpenAI
class GuardrailsAgent:
    def __init__(self, name):
        self.name = name
        self.manager = None
        self.model = model

    def subscribe_to_manager(self, manager):
        self.manager = manager
        self.manager.subscribe(self.name, self.get_subscribed_types())

    def get_subscribed_types(self):
        return ["user"]

    def receive_message(self, message):
        print(f"{self.name} received message: {message}")
        self.process_message(message)

    def process_message(self, message):
        # Generate a prompt for the model based on the received message
        prompt = self.generate_prompt(message)
        # Invoke the OpenAI model with the generated prompt
        response = self.model.invoke([HumanMessage(content=prompt)])
        # Extract the content from the AIMessage object
        response_content = response.content
        # Add the response to the messaging pool
        self.manager.add_message({
            "type": "validation",
            "content": response_content,
            "from": "Guardrails-Agent"
        })

    def generate_prompt(self, message):
        return f"You are a Guardrails Agent. Your role is to ensure the conversation with the user is within scope and advise the Conversation-Agent on standardized messages to use. The message from the user is: {message['content']}. Validate if this message is within guidelines and provide the necessary validation."

# Instantiate agents
conversation_agent = ConversationAgent("Conversation-Agent")
procurement_specialist_agent = ProcurementSpecialistAgent("Procurement-Specialist-Agent")
note_taker_agent = NoteTakerAgent("NoteTaker-Agent")
guardrails_agent = GuardrailsAgent("Guardrails-Agent")

# List of all agents for reference
agents = [conversation_agent, procurement_specialist_agent, note_taker_agent, guardrails_agent]

# Instantiate Messaging Pool Manager
manager = MessagingPoolManager(agents)

# Subscribe agents to the manager
for agent in agents:
    agent.subscribe_to_manager(manager)

# Add initial User message
manager.add_message({"type": "query", "content": "I need to procure laptops for my team.", "from": "user"})

# Process messages with user interaction
while True:
    manager.process_messages()
    user_input = input("Enter your response (or type 'exit' to end): ")
    if user_input.lower() == 'exit':
        break
    manager.add_message({"type": "query", "content": user_input, "from": "user"})

# Print all messages in the pool for verification
print("\nAll messages in the pool:")
for msg in manager.pool:
    print(msg)
