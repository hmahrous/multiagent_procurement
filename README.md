# UBS Multi-Agent Framework

### 1. Project Goal:
Helping the procurement department streamline the process of gathering necessary information from users for form filling to submit a request to the concerned team.

### 2. Desired Inputs and Outputs:
Inputs: User queries, category-specific information requests.
Outputs: A conversation with the user to help complete required forms, structured data for further processing by other systems.

### 3. Specific Requirements or Constraints:
Efficiently capture required information from the user and guide a conversation specialist agent to handle the conversation.
Handle various categories and sub-categories with specific requirements.
Communicate seamlessly among agents.
A specialized agent to communicate with the note taker and the conversation agent, ensuring the fulfillment of the request's requirements.

### 4. Agent Behaviors:

- **Note-Take-Agent:**
    - **Role:** Captures and records the required information based on the specialist agent’s guidelines. Decides whether to add a message to the pool if needed.
    - **Interactions:** Receives instructions from the Procurement-Specialist-Agent about what information needs to be captured from the conversation-agent.
    - **State Updates:** Updates the shared state with new information.


- **Procurement-Specialist-Agent:**
  -**Role:** Provides expertise on specific categories and sub-categories, instructs the Note-Take-Agent on what information to capture next. Decides whether to add a message to the pool if needed.
  - **Interactions:** Receives user inputs through the conversation-agent in the form of queries about a request, then advises on the next steps to capture key information from the user. Advises the conversation-agent on next steps and informs the note taker which information to record. If the user changes the category, it advises on the next actor (another specialized agent).
  - **State Updates:** Ensures required information is being captured as per the category-specific requirements.


- **Guardrails-Agent:**
  - **Role:** Ensures the conversation with the user is within scope and advises the agent on standardized messages to use. Decides whether to add a message to the pool if needed.
  - **Interactions:** Receives updates about user queries and advises on standardized replies if the query does not meet guidelines.
  - **State Updates:** Validates and marks user queries as compliant.


- **Conversation-Agent:**
  - **Role:** Manages the overall flow of the conversation, determines when the interaction has captured all necessary information, and signals the end of the conversation after getting the specialist agent's approval. Decides whether to add a message to the pool if needed.
  - **Interactions:** Monitors state updates and interactions among other agents, decides the flow and end of the conversation.
  - **State Updates:** Finalizes the state when the conversation is complete.

  
**Messaging Pool Manager:** 
  - **Central Message Pool:** All agents are part of the pool. Preconfigure in the state for each agent to indicate who it should subscribe to in order to receive their messages.
  - **Message Passing:** Each agent can read subscribed messages and write to this pool when needed, ensuring all relevant agents receive updates and instructions.
  - **State Management:** LangGraph’s stateful graph system will help maintain and update the shared state across all agents.

## Detailed Interaction Flow Example
### Note-Take-Agent and Procurement-Specialist-Agent Interaction:
- User submits a query.
- Conversation-Agent receives the query and forwards it to the Procurement-Specialist-Agent.
- Procurement-Specialist-Agent determines the next required information and instructs the Note-Take-Agent.
- Note-Take-Agent records the information and updates the state.
- The updated state is shared with the Conversation-Agent and Procurement-Specialist-Agent for further actions.

### Guardrails-Agent Interaction:
- User query is monitored by the Guardrails-Agent.
- If the query is off-topic, the Guardrails-Agent suggests a standardized reply.
- The Conversation-Agent finalizes and sends the reply to the user.

### Conversation-Agent Finalizing Interaction:
- Continuously monitors state updates.
- Once all required information is captured, seeks approval from the Procurement-Specialist-Agent.
- Signals the end of the conversation and finalizes the state.

### Implementation Considerations
- **State Schema:** Must be flexible enough to handle various categories and sub-categories.
- **Message Pool:** Ensure efficient message passing and handling to avoid delays.
- **Error Handling:** Robust mechanisms to handle unexpected inputs or errors in message passing.