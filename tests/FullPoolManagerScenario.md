# Full Interaction Scenario 
 ### 1. User Query:
{ "type": "query", "content": "I need to procure laptops for my team.", "from": "user" }
 ### 2. Conversation-Agent: 
Picks up the query from the pool, forwards it to the Procurement-Specialist-Agent.

{ "type": "query", "content": "I need to procure laptops for my team.", "from": "Conversation-Agent" }

### 3. Procurement-Specialist-Agent:
Determines next steps, sends instructions to both the Conversation-Agent and Note-Take-Agent via the pool.

{ "type": "instruction", "content": "Please ask for laptop specifications such as number of laptops, when was the last time your team changed laptops, RAM requirements, Operating system, is this for project based or a complete replacement.", "from": "Procurement-Specialist-Agent", "to": ["Conversation-Agent", "Note-Take-Agent"] }

### 4. Note-Take-Agent:
Forms a template for the required information and sends it to the pool.

{ "type": "state_update", "content": { "required_info_template": {"num_laptops": "", "last_change": "", "ram_requirements": "", "os": "", "project_based": ""} }, "from": "Note-Take-Agent" }
### 5. Conversation-Agent:
Asks the user for specifications based on the template.

{ "type": "query", "content": "Could you please provide the number of laptops, when was the last time your team changed laptops, RAM requirements, Operating system, and whether this is for a project or a complete replacement?", "from": "Conversation-Agent" }

### 6. User: 
Provides the required information.
{ "type": "response", "content": { "num_laptops": 10, "last_change": "1 year ago", "ram_requirements": "16GB", "os": "Windows 10", "project_based": False }, "from": "user" }

### 7. Note-Take-Agent:
Captures required information, updates state, sends confirmation to pool.
{ "type": "state_update", "content": { "captured_info": {"num_laptops": 10, "last_change": "1 year ago", "ram_requirements": "16GB", "os": "Windows 10", "project_based": False} }, "from": "Note-Take-Agent" }

### 8. Guardrails-Agent:
Validates that the user queries follow the guidelines of the interactions, ensures compliance, sends feedback to pool.

{ "type": "validation", "content": "User request within guidelines.", "from": "Guardrails-Agent" }
## 9. Conversation-Agent:
Monitors state, determines next query or finalizes interaction, updates user via pool.

{ "type": "completion", "content": "All required information gathered.", "from": "Conversation-Agent" }
# 10. Finalization:
Conversation-Agent confirms all information is captured, signals end of conversation via pool.

{ "type": "completion", "content": "All required information gathered.", "from": "Conversation-Agent" }