from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import find_dotenv, load_dotenv
import os
import json
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
import os
from utils import *
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import hashlib
import json
import os



EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
vector_store = "vector_store/"
load_dotenv(find_dotenv())
embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)


def ingest_new_document_vectordb(file_name, content):
    '''
    Ingest a new document to the vector database
    :param file_name:
    :param path:
    '''
    #file_name = file_name.encode("utf-8")
    #file_name = str(file_name)
    encoded_file_name = file_name.encode('utf-8')
    file_hash = hashlib.sha256(encoded_file_name).hexdigest()
    doc = Document(page_content=content, metadata={"file_name": file_name})
    doc = [doc]
    db = FAISS.from_documents(doc, embeddings_model)
    db.save_local(vector_store + file_hash)
    return {'status': 'success'}


def get_vectordb_paths():
    if os.path.exists(vector_store):
        existing_directory_paths = [os.path.join(vector_store, d) for d in os.listdir(vector_store) if os.path.isdir(os.path.join(vector_store, d))]
        return existing_directory_paths
    else:
        return []
    



# for i, dictionary in enumerate(data):
#     print(f"Dictionary {i + 1}:")
#     for key, value in dictionary.items():
#         ingest_new_document_vectordb(str(key), value)

