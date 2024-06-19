from typing import Dict, List
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import find_dotenv, load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
import hashlib
import os

EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
VECTOR_STORE_DIR = "vector_store/"

load_dotenv(find_dotenv())
embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)

def ingest_new_document_vectordb(file_name: str, content: str) -> Dict[str, str]:
    """
    Ingest a new document to the vector database.
    :param file_name: The name of the file.
    :param content: The content of the document.
    :return: Status of the ingestion.
    """
    encoded_file_name = file_name.encode('utf-8')
    file_hash = hashlib.sha256(encoded_file_name).hexdigest()
    doc = Document(page_content=content, metadata={"file_name": file_name})
    db = FAISS.from_documents([doc], embeddings_model)
    db.save_local(os.path.join(VECTOR_STORE_DIR, file_hash))
    return {'status': 'success'}

def get_vectordb_paths() -> List[str]:
    """
    Get the paths of existing vector databases.
    :return: List of paths.
    """
    if os.path.exists(VECTOR_STORE_DIR):
        return [os.path.join(VECTOR_STORE_DIR, d) for d in os.listdir(VECTOR_STORE_DIR) if os.path.isdir(os.path.join(VECTOR_STORE_DIR, d))]
    return []
