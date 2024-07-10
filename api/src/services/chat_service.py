import sys
from typing import Any, Sequence, Union

from openai import AsyncOpenAI
from sqlalchemy import Row, RowMapping, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.config import get_settings
from src.models.chat import Chat
from src.schemas.responses import ChatOutput

# Initialise asynchronous openAI client

try:
    client = AsyncOpenAI(api_key=get_settings().open_ai_config.openai_api_key)

except Exception as error:
    print(
        f"Error - {error}. Hint: If running locally, Make sure the OpenAI api key is present in .env file"
    )
    sys.exit()


class ChatApp:
    def __init__(self, pool_manager):
        self.pool_manager = pool_manager

    async def main(self, message):
        if not self.pool_manager.pool:
            await self.pool_manager.add_user_message("", message.content)
        else:
            await self.pool_manager.process_messages()


async def get_openai_response(input_prompt: str, session: AsyncSession) -> ChatOutput:
    """
    Get response from openAI API and add data to chat history.
    @param input_prompt:
    @param session:
    @return:
    """
    # Add to database
    chat_object = Chat(prompt=input_prompt)
    session.add(chat_object)
    await session.commit()

    # Example implementation of calling openAI to get response

    # -----------------------------------------------------------------------------#
    # In case custom prompts needs to be used with or without knowledge corpus
    # from prompts import dummy_prompt
    # prompt_to_openAI = prompts.dummy_prompt(role='user', data='dummy data')
    # -----------------------------------------------------------------------------

    prompt = [{"role": "user", "content": input_prompt}]

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo", messages=prompt, max_tokens=100
    )

    return ChatOutput(response=response.choices[0].message.content)


async def get_history(
    session: AsyncSession,
) -> Sequence[Union[Union[Row[Any], RowMapping], Any]]:
    """
    Get prompt history from database
    @param session:
    @return:
    """
    statement = select(Chat)
    result = await session.scalars(statement)
    return result.all()


# Example implementation of removing data from database using SQL Alchemy
async def delete_history(session: AsyncSession) -> None:
    """
    Delete prompt history from database
    @param session:
    """
    await session.execute(delete(Chat))
    await session.commit()
