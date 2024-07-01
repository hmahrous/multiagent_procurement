# -*- coding: utf-8 -*-
from fastapi import APIRouter, File, UploadFile
import time
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from Agents import agents
from MessagingPoolManager import MessagingPoolManager
import uuid
from fastapi.responses import JSONResponse


class TextInput(BaseModel):
    text: str

class IdInput(BaseModel):
    id: str

class ModeInput(BaseModel):
    mode: str

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.last_time_used = {}

    def get_session(self, session_id: str):
        current_time = time.time()
        if session_id not in self.sessions or (session_id in self.last_time_used and current_time - self.last_time_used[session_id] > 3600):
            self.sessions[session_id] = MessagingPoolManager(agents)
            self.last_time_used[session_id] = current_time
        return self.sessions[session_id]

session_manager = SessionManager()

document_router = APIRouter()

@document_router.post("/user")
async def stream_text(input: TextInput, session_id: IdInput, mode: ModeInput):
    custom_agent = session_manager.get_session(session_id.id)
    prompt = f"""{input.text}"""
    #print(prompt)
    await custom_agent.add_user_message("", prompt)
    response = await custom_agent.process_messages(mode=mode.mode)
    return JSONResponse(content=response) # if mode.mode == "group" else [response]


@document_router.get("/new_session/")
def new_session():
    session_id = str(uuid.uuid4())
    session_manager.get_session(session_id)
    return {"session_id": session_id}






# from fastapi import APIRouter, File, UploadFile
# import time
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from Agents import agents
# from MessagingPoolManager import pool_manager
# import uuid
# from dotenv import load_dotenv
# from fastapi.responses import JSONResponse


# class TextInput(BaseModel):
#     text: str

# class IdInput(BaseModel):
#     id: str

# class SessionManager:
#     def __init__(self):
#         self.sessions = {}
#         self.last_time_used = {}

#     def get_session(self, session_id: str):
#         current_time = time.time()
#         if session_id not in self.sessions or (session_id in self.last_time_used and current_time - self.last_time_used[session_id] > 3600):
#             self.sessions[session_id] = pool_manager(agents)
#             self.last_time_used[session_id] = current_time
#         return self.sessions[session_id]

# session_manager = SessionManager()

# document_router = APIRouter()

# @document_router.post("/user")
# async def stream_text(input: TextInput, session_id: IdInput):
#     custom_agent = session_manager.get_session(session_id.id)
#     prompt = f"""user_text:{input.text}"""  #user_session_id: {session_id.id}
#     return StreamingResponse(custom_agent.add_user_message("", prompt), media_type="text/plain")


# @document_router.get("/new_session/")
# def new_session():
#     session_id = str(uuid.uuid4())
#     session_manager.get_session(session_id)
#     return {"session_id": session_id}

