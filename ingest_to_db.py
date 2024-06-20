import json
from typing import Dict
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import find_dotenv, load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
import hashlib
import os
import shutil

load_dotenv(find_dotenv())
VECTOR_STORE_DIR = "vector_store/"
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

def ingest_new_document_vectordb(identifier: str, content: str) -> Dict[str, str]:
    """
    Ingest a new document to the vector database.
    :param identifier: The name of the file.
    :param content: The content of the document.
    :return: Status of the ingestion.
    """
    encoded_file_name = identifier.encode('utf-8')
    file_hash = hashlib.sha256(encoded_file_name).hexdigest()
    doc = Document(page_content=content, metadata={"identifier": identifier})
    db = FAISS.from_documents([doc], embeddings_model)
    db.save_local(os.path.join(VECTOR_STORE_DIR, file_hash))
    return {'status': 'success'}

def clear_vector_store(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def ingest_json_vectordb(data, mode: str = 'append') -> Dict[str, str]:
    if mode == 'overwrite':
        clear_vector_store(VECTOR_STORE_DIR)
    for identifier, content in data.items():
        result = ingest_new_document_vectordb(identifier, content)
        print(f"Ingested {identifier}: {result['status']}")


if __name__ == "__main__":
    json_file_path = "json_file.json"
    mode = 'overwrite'  # Change to 'append' if you want to append instead of overwrite
    with open(json_file_path, "r") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("The JSON data must be a dictionary with identifiers as keys and content as values.")
    result = ingest_json_vectordb(data, mode)
    print(f"Ingestion completed: {result['status']}")
