import uuid
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.endpoints import SessionManager
from src.schemas.requests import ChatInput, ModeInput, idInput

session_manager = SessionManager()
router = APIRouter()

@router.post(
    "/message",
)
async def chat_with_gpt(input_data: ChatInput, session_id: idInput, mode: ModeInput):
    logging.info(f"Received input_data: {input_data}")
    logging.info(f"Received session_id: {session_id}")
    logging.info(f"Received mode: {mode}")

    custom_agent = session_manager.get_session(session_id.id_)
    await custom_agent.add_user_message("", f"""{input_data.message}""")
    response = await custom_agent.process_messages(mode=mode.mode)

    #logging.info(f"Response from custom_agent.process_messages: {response}")
    return JSONResponse(content=response)


@router.get("/create_session")
def create_session():
    session_id = str(uuid.uuid4())
    session_manager.get_session(session_id)
    logging.info(f"Created new session with ID: {session_id}")
    return {"session_id": session_id}
