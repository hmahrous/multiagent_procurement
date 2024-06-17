from typing import Annotated
from langchain_core.tools import tool
from utils import *
from typing import Annotated, Dict, Union, List, Optional
from typing_extensions import TypedDict
from State import initial_state

@tool
def knowledge_base_tool(
    theme: Annotated[str, "The theme of the user's question."] = ''
) -> Annotated[str, "Concatenated texts from the similarity search results."]:
    """
    This tool will load the knowledge base that will be used to answer requests.
    :param theme: The theme of the user's question.
    :return: Concatenated texts from the similarity search results.
    """
    print('knowledge base call')
    db_paths = get_vectordb_paths()
    print(f'The length of the paths is: {len(db_paths)}')
    if not db_paths:
        return None

    for i, db_path in enumerate(db_paths):
        if i == 0:
            db = FAISS.load_local(db_path, embeddings_model, allow_dangerous_deserialization=True)
        else:
            db_next = FAISS.load_local(
                db_path, embeddings_model, allow_dangerous_deserialization=True)
            db.merge_from(db_next)

    docs = db.similarity_search(theme, 2)
    texts = [doc.page_content for doc in docs]
    return '\n'.join(texts)