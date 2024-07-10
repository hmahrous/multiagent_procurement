import chainlit as cl

from src.services.agents_service import initialize_agents
from src.services.chat_service import ChatApp
from src.services.pool_service import MessagingPoolManager

agents = initialize_agents()
pool_manager = MessagingPoolManager(agents)
chat_app = ChatApp(pool_manager)


@cl.on_message
async def main(message):
    await chat_app.main(message)
