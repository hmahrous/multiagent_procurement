# ----------------------------------------------------------------------------------------------------------------#
# This is an example async implementation of using vector capabilities                                            #
# of postgres using extension pgvector and langchain.                                                             #
# For information about available functions, refer to                                                             #
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.pgvector.PGVector.html #
# ----------------------------------------------------------------------------------------------------------------#

import hashlib
import json
import os
import pdb
import shutil
from typing import Dict, List

from dotenv import find_dotenv, load_dotenv
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from src.core.config import get_settings
from src.schemas.requests import MetaData
from src.schemas.responses import StoreChunksOutput

load_dotenv(find_dotenv())


EMBEDDING = OpenAIEmbeddings()
NUMBER_OF_CHUNKS_CONSIDERED = 5
MINIMUM_RELEVANCE_SCORE = 0.8
POSTGRES_COLLECTION_NAME = "test_vector_table"
try:
    DATABASE_URL = get_settings().sqlalchemy_sync_database_uri.render_as_string(
        hide_password=False
    )
except:
    DATABASE_URL = ""


class VectorStore_local_faiss:
    """A class that wraps Vector store implementation of FAISS"""

    def __init__(self):
        load_dotenv(find_dotenv())
        self.EMBEDDING_MODEL_NAME = "text-embedding-3-large"
        self.VECTOR_STORE_DIR = "knowledge_base/local_faiss_vector_store/"
        self.knowledgebase_json_file = (
            "knowledge_base/big_software_process_new_request_no_risk.json"
        )
        # check if directory exist if not create
        if not os.path.exists(self.VECTOR_STORE_DIR):
            os.makedirs(self.VECTOR_STORE_DIR)
        self.embeddings_model = OpenAIEmbeddings(model=self.EMBEDDING_MODEL_NAME)
        self.run_json_ingestion(mode="overwrite")

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


class VectorStore_postgres:
    """A class that wraps Vector store implementation of Postgres"""

    def __init__(self):
        self._pg_vector_db = None

    def get_vector_db(self):
        """
        Get pg_vector db instance
        @return:
        """
        if not self._pg_vector_db:
            self._pg_vector_db = PGVector(
                collection_name=POSTGRES_COLLECTION_NAME,
                connection_string=DATABASE_URL,
                embedding_function=EMBEDDING,
            )
        return self._pg_vector_db

    async def query(self, query: str) -> dict:
        """
        Query vector store to find similar documents with relevance score.
        @param query:
        @return:
        """
        result = await self.get_vector_db().asimilarity_search_with_relevance_scores(
            query,
            k=NUMBER_OF_CHUNKS_CONSIDERED,
            score_threshold=MINIMUM_RELEVANCE_SCORE,
        )
        return {"chunks": result}

    async def store_chunks(
        self, texts: List[str], metadata: List[MetaData]
    ) -> StoreChunksOutput:
        """
        Store chunks to vector store.
        @param texts:
        @param metadata:
        @return:
        """
        stripped_texts = [txt.replace("\n", " ") for txt in texts]

        result = await self.get_vector_db().aadd_texts(
            texts=stripped_texts, metadatas=[{"page": i.page} for i in metadata]
        )
        return StoreChunksOutput(UUIDS=result)

    @staticmethod
    async def delete_chunks(session: AsyncSession) -> None:
        """
        Delete chunks from vector store
        @param session:
        """
        # The query can be changed as per the needs. Here is the sample implementation of filtering data.
        query = text("select uuid from langchain_pg_embedding")
        result = await session.scalars(query)
        uuids = result.all()

        if len(uuids):
            # Deleting chunks fromm vector store
            query = text(f"Delete from langchain_pg_embedding")
            await session.execute(query)
            await session.commit()


vector_store_faiss = VectorStore_local_faiss()
vector_store = VectorStore_postgres()
