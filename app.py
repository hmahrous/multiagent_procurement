import chainlit as cl
from Agents import pool_manager, run_agents, initial_state

@cl.on_message
async def main(message: str):
    user_query = {"type": "query", "content": message, "from": "user", "role": "user"}
    initial_state["user_query"] = user_query["content"]
    pool_manager.add_message(user_query)
    initial_state["user_query"] = message
    initial_state["query_fulfilled"]=False
    response = run_agents()
    return response

if __name__ == "__main__":
    cl.launch()
