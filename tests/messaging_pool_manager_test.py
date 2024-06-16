from MessagingPoolManager import MessagingPoolManager
from Agents import ConversationAgentDummy, ProcurementSpecialistAgentDummy, NoteTakerAgentDummy, GuardrailsAgentDummy

# Instantiate Agents
conversation_agent = ConversationAgentDummy("Conversation-Agent")
procurement_specialist_agent = ProcurementSpecialistAgentDummy("Procurement-Specialist-Agent")
note_taker_agent = NoteTakerAgentDummy("NoteTaker-Agent")
guardrails_agent = GuardrailsAgentDummy("Guardrails-Agent")

# List of all agents for reference
agents = [conversation_agent, procurement_specialist_agent, note_taker_agent, guardrails_agent]

# Instantiate Messaging Pool Manager
manager = MessagingPoolManager(agents)

# Subscribe agents to the manager
for agent in agents:
    agent.subscribe_to_manager(manager)

# Add initial User message
manager.add_message({"type": "query", "content": "I need to procure laptops for my team.", "from": "user"})

# Process messages
for _ in range(4):  # Loop a few times to ensure all messages are processed
    manager.process_messages()


# Print all messages in the pool for verification
print("\nAll messages in the pool:")
for msg in manager.pool:
    print(msg)
