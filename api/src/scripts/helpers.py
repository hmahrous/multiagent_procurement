from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
import hashlib
import json
import os
from openai import OpenAI
import numpy as np
from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import asyncio
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS, DistanceStrategy
from src.services.vector_service import EMBEDDING_MODEL_NAME, VECTOR_STORE_DIR, HASH_MAPPING_FILE

distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT
embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME)
gpt4_o = ChatOpenAI(temperature=0, model="gpt-4o")


SYSTEM_PROMPT = """Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
context.
1. Split compound sentence into simple sentences. Maintain the original phrasing from the input
whenever possible.
2. For any named entity that is accompanied by additional descriptive information, separate this
information into its own distinct proposition.
3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that") with the full name of the
entities they refer to.
4. Present the results as a list of strings, formatted in JSON.
Input: Title: Eostre. Section: Theories and interpretations, Connection to Easter Hares. Content: ¯
The earliest evidence for the Easter Hare (Osterhase) was recorded in south-west Germany in
1678 by the professor of medicine Georg Franck von Franckenau, but it remained unknown in
other parts of Germany until the 18th century. Scholar Richard Sermon writes that "hares were
frequently seen in gardens in spring, and thus may have served as a convenient explanation for the
origin of the colored eggs hidden there for children. Alternatively, there is a European tradition
that hares laid eggs, since a hare’s scratch or form and a lapwing’s nest look very similar, and
both occur on grassland and are first seen in the spring. In the nineteenth century the influence
of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular throughout Europe.
German immigrants then exported the custom to Britain and America where it evolved into the
Easter Bunny."
Output: [ "The earliest evidence for the Easter Hare was recorded in south-west Germany in
1678 by Georg Franck von Franckenau.", "Georg Franck von Franckenau was a professor of
medicine.", "The evidence for the Easter Hare remained unknown in other parts of Germany until
the 18th century.", "Richard Sermon was a scholar.", "Richard Sermon writes a hypothesis about
the possible explanation for the connection between hares and the tradition during Easter", "Hares
were frequently seen in gardens in spring.", "Hares may have served as a convenient explanation
for the origin of the colored eggs hidden in gardens for children.", "There is a European tradition
that hares laid eggs.", "A hare’s scratch or form and a lapwing’s nest look very similar.", "Both
hares and lapwing’s nests occur on grassland and are first seen in the spring.", "In the nineteenth
century the influence of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular
throughout Europe.", "German immigrants exported the custom of the Easter Hare/Rabbit to
Britain and America.", "The custom of the Easter Hare/Rabbit evolved into the Easter Bunny in
Britain and America." ]
"""

async def decompose_content_chain(chunk_list):
    system_message_prompt = SystemMessagePromptTemplate(prompt=PromptTemplate(template=SYSTEM_PROMPT, input_variables=[]))
    HUMAN_PROMPT = '''
        Input: {text}
        Output:
    '''
    human_message_prompt = HumanMessagePromptTemplate.from_template(HUMAN_PROMPT)
    chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    async def generate_fact(content):
        chat_prompt_with_values = chat_prompt_template.format_prompt(text=content)
        response = await gpt4_o.agenerate([chat_prompt_with_values.to_messages()])
        # Extract the text from the response
        return response.generations[0][0].text

    tasks = [generate_fact(chunk['content_with_weight']) for chunk in chunk_list if 'content_with_weight' in chunk]
    facts = await asyncio.gather(*tasks)
    print(f"here are the facts {facts}")
    return facts

def get_ingested_filenames():
    if os.path.exists(HASH_MAPPING_FILE):
        with open(HASH_MAPPING_FILE, "r", encoding='utf-8') as f:
            hash_to_filename_mapping = json.load(f)
            filenames = list(hash_to_filename_mapping.keys())
            return filenames
    return []

async def ingest_new_document_vectordb(file_name, chunks):
    if not isinstance(chunks, list):
        chunks = [chunks]
    # Process content in parallel
    texts = await decompose_content_chain(chunks)
    db = FAISS.from_texts(texts, embeddings_model, distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
    encoded_file_name = file_name.encode('utf-8')
    vector_store_path = os.path.abspath(VECTOR_STORE_DIR)
    file_hash = hashlib.sha256(encoded_file_name).hexdigest()
    db.save_local(os.path.join(vector_store_path, file_hash))
    __save_hash_to_filename_mapping(file_hash, file_name)
    return {'status': 'success'}


def __save_hash_to_filename_mapping(file_hash, original_file_name):
    if os.path.exists(HASH_MAPPING_FILE):
        with open(HASH_MAPPING_FILE, "r", encoding='utf-8') as f:
            hash_to_filename_mapping = json.load(f)
    else:
        hash_to_filename_mapping = {}
    hash_to_filename_mapping[original_file_name] = file_hash
    with open(HASH_MAPPING_FILE, "w", encoding='utf-8') as f:
        json.dump(hash_to_filename_mapping, f, ensure_ascii=False)

def delete_file_vectordb(filename):
    if os.path.exists(HASH_MAPPING_FILE):
        with open(HASH_MAPPING_FILE, "r", encoding='utf-8') as f:
            hash_to_filename_mapping = json.load(f)
        
        if filename in hash_to_filename_mapping:
            file_hash = hash_to_filename_mapping[filename]
            os.remove(os.path.join(VECTOR_STORE_DIR, file_hash))
            del hash_to_filename_mapping[filename]
            
            with open(HASH_MAPPING_FILE, "w", encoding='utf-8') as f:
                json.dump(hash_to_filename_mapping, f, ensure_ascii=False)
            
            return {'status': 'success'}
        else:
            return {'status': 'filename not found'}
    else:
        return {'status': 'mapping file not found'}

# def __check_file_name(file_name):
#     if os.path.exists(HASH_MAPPING_FILE):
#         with open(HASH_MAPPING_FILE, "r", encoding='utf-8') as f:
#             hash_to_filename_mapping = json.load(f)
#             return str(file_name) in hash_to_filename_mapping
#     return False





# def ingest_new_document_vectordb(file_name, chunks):
#     if not isinstance(chunks, list):
#         chunks = [chunks]
#     texts = decompose_content_chain(chunks)

#     db = FAISS.from_texts(texts, embeddings_model, distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)

#     encoded_file_name = file_name.encode('utf-8')

#     file_hash = hashlib.sha256(encoded_file_name).hexdigest()

#     db.save_local(os.path.join(VECTOR_STORE_DIR, file_hash))

#     __save_hash_to_filename_mapping(file_hash, file_name)

#     return {'status': 'success'}