from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
import json
import os
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv(override=True)

open_ai_endpoint = os.getenv('OPENAI_ENDPOINT')
open_ai_key = os.getenv('OPENAI_KEY')
open_ai_embedding_model = os.getenv('EMBEDDING_OPENAI_DEPLOYMENT')
open_ai_version = os.getenv('OPENAI_API_VERSION')

search_endpoint = os.getenv('SEARCH_ENDPOINT')
search_api_key = os.getenv('SEARCH_API_KEY')

dataset_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(dataset_dir, '..', '..')
lore_file_path = os.path.join(project_root, 'dataset', 'lore.json')

openai = AzureOpenAI(
    azure_endpoint=open_ai_endpoint,
    api_key=open_ai_key,
    api_version="2024-12-01-preview"
)

def embed_document(file_path:str, field_name:str, vector_field_name:str) -> list:
    
    with open(file_path,'r',encoding='utf-8') as f:
        datas = json.load(f)

    documents = []

    logging.info(f"{len(datas)} documents to upload")

    for data in datas:

        text_to_embed = data[field_name]
        response = openai.embeddings.create(input=text_to_embed, model=open_ai_embedding_model)

        data[vector_field_name] = response.data[0].embedding

        documents.append(data)

        time.sleep(1)

    logging.info(f"{len(documents)} vectorized")

    return documents

def upload_documents(index_name:str, docs:list):
    
    search_client = SearchClient(endpoint=search_endpoint,
                                index_name=index_name,
                                credential=AzureKeyCredential(search_api_key))
    
    result = search_client.upload_documents(docs)

    logging.info(f"Uploaded of document success: {result[0].succeeded}")

    search_client.close()

def main():
    
    documents = embed_document(lore_file_path,'content','content_vector')

    upload_documents("lore",documents)


if __name__ == "__main__":
    main()
