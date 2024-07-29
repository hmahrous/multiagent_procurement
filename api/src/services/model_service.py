import os
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from src.core.config import get_settings
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GPT_DEPLOYMENT_ENV = os.getenv("DEPLOYMENT_ENV")

def get_llm_model():
    if GPT_DEPLOYMENT_ENV == "AzureOpenAI":
        llm = AzureChatOpenAI(api_version= os.getenv("AZURE_OPENAI_API_VERSION"),
                              azure_endpoint= os.getenv("AZURE_OPENAI_API_URL"),
                              openai_api_key= os.getenv("AZURE_OPENAI_API_KEY"),
                              azure_deployment= "gpt4")
    else:
        llm = ChatOpenAI(model="gpt-4o")
    return llm

def get_embedding_model():
    if GPT_DEPLOYMENT_ENV == "AzureOpenAI":
        embedding = AzureOpenAIEmbeddings(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_URL"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_deployment="gpt35_16k")
    else:
        embedding = OpenAIEmbeddings(model="text-embedding-3-large")
    return embedding