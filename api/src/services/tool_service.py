import os
from typing import Annotated

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain_core.tools import tool
from src.services.vector_service import EMBEDDING_MODEL_NAME, VECTOR_STORE_DIR
from typing import Dict, List



# @tool
# async def knowledge_base_tool_(
#     theme: Annotated[str, "The theme of the user's question."] = "",
# ) -> Annotated[str, "Concatenated texts from the similarity search results."]:
#     """
#     This tool will load the knowledge base that will be used to answer requests.
#     :param theme: The theme of the user's question.
#     :return: Concatenated texts from the similarity search results.
#     """
#     search_result = await vector_store.query(theme)

#     if not search_result["chunks"]:
#         return "No relevant information found."

#     relevant_texts = []
#     for chunk in search_result["chunks"]:
#         relevant_texts.append(chunk["text"])
#     return "\n".join(relevant_texts)

class knowledge_base_tool_faiss():
    def __init__(self):
        empty_string = ''
        print('knowledge base call')
        db_paths = self.get_directory_paths(VECTOR_STORE_DIR)
        embeddings_model = EMBEDDING_MODEL_NAME
        embeddings_model = OpenAIEmbeddings(model=embeddings_model)
        if not db_paths:
            return empty_string
        self.db = None
        for i, db_path in enumerate(db_paths):
            if i == 0:
                self.db = FAISS.load_local(db_path, embeddings_model, allow_dangerous_deserialization=True)
            else:
                db_next = FAISS.load_local(db_path, embeddings_model, allow_dangerous_deserialization=True)
                self.db.merge_from(db_next)

    def get_directory_paths(self, directory: str) -> list:
        """
        Get a list of folder paths within the specified directory.
        :param directory: The path to the directory.
        :return: A list of folder paths.
        """
        folder_paths = []
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                folder_paths.append(os.path.join(root, name))
        return folder_paths

class FaissDBConnection:
    _instance = None

    def __new__(cls):
        """
        Create a new instance of the class or return the existing one.

        This method implements the singleton pattern, which ensures that only one instance of the class exists.
        It loads local FAISS models from directories and merges them into a single instance.

        :return: The singleton instance of the class.
        """
        if cls._instance is None:
            # Get a list of folder paths within the specified directory.
            db_paths = []
            directory = VECTOR_STORE_DIR
            for root, dirs, files in os.walk(directory):
                for name in dirs:
                    db_paths.append(os.path.join(root, name))
            embeddings_model = EMBEDDING_MODEL_NAME
            embeddings_model = OpenAIEmbeddings(model=embeddings_model)
            if not db_paths:
                return
            for i, db_path in enumerate(db_paths):
                if i == 0:
                    cls._instance = FAISS.load_local(
                        db_path, embeddings_model, allow_dangerous_deserialization=True
                    )
                else:
                    db_next = FAISS.load_local(
                        db_path, embeddings_model, allow_dangerous_deserialization=True
                    )
                    cls._instance.merge_from(db_next)
        return cls._instance

@tool
def tool_runner(
    theme: Annotated[str, "The theme of the user's question."] = ""
) -> Annotated[str, "Concatenated texts from the similarity search results."]:
    """
    This tool will load the knowledge base that will be used to answer requests.
    :param theme: The theme of the user's question.
    :return: Concatenated texts from the similarity search results.
    """
    empty_string = ""
    print("knowledge base call")
    db = FaissDBConnection()
    docs = db.similarity_search(theme)
    texts = [doc.page_content for doc in docs]
    return "******Knowledge Base RAG output:******\n\n" + "\n".join(texts)



# def get_vectordb_paths() -> List[str]:
#     """
#     Get the paths of existing vector databases.
#     :return: List of paths.
#     """
#     if os.path.exists(VECTOR_STORE_DIR):
#         return [os.path.join(VECTOR_STORE_DIR, d) for d in os.listdir(VECTOR_STORE_DIR) if os.path.isdir(os.path.join(VECTOR_STORE_DIR, d))]
#     return []

# @tool
# def knowledge_base_tool(
#     theme: Annotated[str, "The theme of the user's question."] = ''
# ) -> Annotated[str, "Concatenated texts from the similarity search results."]:
#     """
#     This tool will load the knowledge base that will be used to answer requests.
#     :param theme: The theme of the user's question.
#     :return: Concatenated texts from the similarity search results.
#     """
#     print('knowledge base call')
#     db_paths = get_vectordb_paths()
#     print(f'The length of the paths is: {len(db_paths)}')
#     if not db_paths:
#         return None
#     embeddingss = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
#     db = None
#     for i, db_path in enumerate(db_paths):
#         if i == 0:
#             db = FAISS.load_local(db_path, embeddingss, allow_dangerous_deserialization=True)
#         else:
#             db_next = FAISS.load_local(db_path, embeddingss, allow_dangerous_deserialization=True)
#             db.merge_from(db_next)
#     if db is None:
#         return ""
#     docs = db.similarity_search(theme)
#     texts = [doc.page_content for doc in docs]
#     return "******Knowledge Base RAG output:******\n\n" + "\n".join(texts)