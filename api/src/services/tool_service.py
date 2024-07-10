from typing import Annotated
from langchain_core.tools import tool
from langchain.vectorstores.faiss import FAISS
from src.services.vector_service import vector_store , vector_store_faiss
import os
from langchain.embeddings.openai import OpenAIEmbeddings

def get_folder_paths(directory: str) -> list:
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

@tool
async def knowledge_base_tool_(
    theme: Annotated[str, "The theme of the user's question."] = "",
) -> Annotated[str, "Concatenated texts from the similarity search results."]:
    """
    This tool will load the knowledge base that will be used to answer requests.
    :param theme: The theme of the user's question.
    :return: Concatenated texts from the similarity search results.
    """
    search_result = await vector_store.query(theme)

    if not search_result["chunks"]:
        return "No relevant information found."

    relevant_texts = []
    for chunk in search_result["chunks"]:
        relevant_texts.append(chunk["text"])
    return "\n".join(relevant_texts)


@tool
def knowledge_base_tool_faiss(
    theme: Annotated[str, "The theme of the user's question."] = ''
) -> Annotated[str, "Concatenated texts from the similarity search results."]:
    """
    This tool will load the knowledge base that will be used to answer requests.
    :param theme: The theme of the user's question.
    :return: Concatenated texts from the similarity search results.
    """
    empty_string = ''
    print('knowledge base call')
    db_paths = get_folder_paths(vector_store_faiss.get_VECTOR_STORE_DIR())
    embeddings_model = vector_store_faiss.get_EMBEDDING_MODEL_NAME()
    embeddings_model = OpenAIEmbeddings(model=embeddings_model)
    print(f'The length of the paths is: {len(db_paths)}')
    if not db_paths:
        return empty_string
    db = None
    for i, db_path in enumerate(db_paths):
        if i == 0:
            db = FAISS.load_local(db_path, embeddings_model, allow_dangerous_deserialization=True)
        else:
            db_next = FAISS.load_local(db_path, embeddings_model, allow_dangerous_deserialization=True)
            db.merge_from(db_next)

    if db is None:
        return empty_string

    print(db)
    docs = db.similarity_search(theme)
    texts = [doc.page_content for doc in docs]
    return "******Knowledge Base RAG output:******\n\n" + '\n'.join(texts)
