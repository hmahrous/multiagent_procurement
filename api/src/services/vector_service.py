import hashlib
import json
import os
import pdb
import shutil
from typing import Dict, List
from dotenv import find_dotenv, load_dotenv
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS
from src.services.model_service import get_embedding_model

load_dotenv(find_dotenv())

VECTOR_STORE_DIR = "/api/knowledge_base/vector_store"
HASH_MAPPING_FILE = "/api/knowledge_base/hash_mapping.json"


class VectorStore_local_faiss:
    """A class that wraps Vector store implementation of FAISS"""

    def __init__(self):
        load_dotenv(find_dotenv())
        self.VECTOR_STORE_DIR = "knowledge_base/local_faiss_vector_store/"
        self.knowledgebase_json_file = (
            "knowledge_base/big_software_process_new_request_no_risk.json"
        )
        # check if directory exist if not create
        if not os.path.exists(self.VECTOR_STORE_DIR):
            os.makedirs(self.VECTOR_STORE_DIR)
        self.embeddings_model = get_embedding_model()
        #self.run_json_ingestion(mode="overwrite")

    def _ingest_new_document_vectordb(self, identifier: str, content: str) -> Dict[str, str]:
        """
        Ingest a new document to the vector database.
        :param identifier: The name of the file.
        :param content: The content of the document.
        :return: Status of the ingestion.
        """
        encoded_file_name = identifier.encode("utf-8")
        file_hash = hashlib.sha256(encoded_file_name).hexdigest()
        doc = Document(page_content=content, metadata={"identifier": identifier})
        db = FAISS.from_documents([doc], self.embeddings_model)

        # Ensure the VECTOR_STORE_DIR is an absolute path
        vector_store_path = os.path.abspath(self.VECTOR_STORE_DIR)
        print("Current working directory:", os.getcwd())
        save_path = os.path.join(vector_store_path, file_hash)
        print(f"Saving to {save_path}")

        db.save_local(save_path)
        return {"status": "success"}

    def _clear_vector_store(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)

    def ingest_json_vectordb(self, data, mode: str = "overwrite") -> Dict[str, str]:
        if mode == "overwrite":
            self._clear_vector_store(self.VECTOR_STORE_DIR)
        for dict_ in data:
            for identifier, content in dict_.items():
                result = self._ingest_new_document_vectordb(identifier, content)
                print(f"Ingested {identifier}: {result['status']}")
        return {"status": "success"}

    def run_json_ingestion(self, mode: str = "overwrite") -> Dict[str, str]:
        with open(self.knowledgebase_json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        result = self.ingest_json_vectordb(data, mode)
        print(f"Ingestion completed: {result['status']}")
        return result

    def get_VECTOR_STORE_DIR(self):
        return self.VECTOR_STORE_DIR

    def get_EMBEDDING_MODEL_NAME(self):
        return self.EMBEDDING_MODEL_NAME

vector_store_faiss = VectorStore_local_faiss()
