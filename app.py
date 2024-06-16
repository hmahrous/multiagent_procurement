import chainlit as cl
from State import initial_state
from Agents import pool_manager, run_agents

@cl.on_message
async def main(message: cl.message):
    print(message)
    user_query = {"type": "query", "content": message.content, "from": "user", "role": "user"}
    pool_manager.add_message(user_query)
    initial_state["user_query"] = message.content
    initial_state["query_fulfilled"]=False
    response = run_agents()
    await cl.Message(content=response).send()


if __name__ == "__main__":
    cl.launch()
