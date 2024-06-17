import chainlit as cl
from MessagingPoolManager import pool_manager




# Chainlit app
@cl.on_message
async def main(message):
    if not pool_manager.pool:
        await pool_manager.add_user_message(message.content)
    else:
        await pool_manager.process_messages()