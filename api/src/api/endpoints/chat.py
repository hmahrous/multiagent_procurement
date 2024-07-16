import uuid
import logging
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import shutil
import os
from src.api.endpoints import SessionManager
from src.schemas.requests import ChatInput, ModeInput, idInput
from src.scripts.helpers import ingest_new_document_vectordb, get_ingested_filenames, delete_file_vectordb
from langchain_community.document_loaders import PyPDFLoader
from uuid import uuid4
import json

def dummy(prog=None, msg=""):
    pass

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
    response, initial_state = await custom_agent.process_messages(mode=mode.mode)

    return JSONResponse(content={"response": response, "schema_": initial_state})

@router.get("/create_session")
def create_session():
    session_id = str(uuid.uuid4())
    session_manager.get_session(session_id)
    logging.info(f"Created new session with ID: {session_id}")
    return {"session_id": session_id}


@router.post("/ingest_document/")
async def ingest_document(file: UploadFile = File(...)):
    logging.info(f'file path is {file.filename}')
    try:
        # Create a temporary file path
        temp_file_path = f"/tmp/{file.filename}"
        # Save the uploaded file to the temporary location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Process the file based on its extension
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(temp_file_path)
            chunks = loader.load_and_split()
            print(f'length of chunks is {len(chunks)}')
            chunks = [{"content_with_weight": str(page.page_content)} for page in chunks]
            print(f'sample chunk is {chunks[0]}')
            #chunks = chunk(temp_file_path, lang="English", callback=dummy)
        elif file.filename.endswith(".json"):
            with open(temp_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    chunks = [{"content_with_weight": str(list(item.values())[0])} for item in data]
                else:
                    os.remove(temp_file_path)
                    return {"error": "Invalid JSON format"}
        else:
            os.remove(temp_file_path)
            return {"error": "Unsupported file format"}

        logging.info(f'chunks processed successfully with a length of: {len(chunks)}')
        # Ingest the document into the vector database
        result = await ingest_new_document_vectordb(file.filename, chunks)
        # Clean up the temporary file
        os.remove(temp_file_path)
        return result
    except Exception as e:
        # Ensure the temporary file is removed in case of an error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/list_documents/", response_model=List[str])
def list_documents_endpoint():
    try:
        documents = get_ingested_filenames()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_document/")
async def delete_document(file_name: str):
    try:
        result = delete_file_vectordb(file_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))