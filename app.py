# app.py

import chainlit as cl
from MessagingPoolManager import pool_manager

class ChatApp:
    def __init__(self, pool_manager):
        self.pool_manager = pool_manager

    async def main(self, message):
        if not self.pool_manager.pool:
            await self.pool_manager.add_user_message("", message.content)
        else:
            await self.pool_manager.process_messages()

chat_app = ChatApp(pool_manager)

@cl.on_message
async def main(message):
    await chat_app.main(message)
