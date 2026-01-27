from azure.identity import AzureCliCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import requests
import json
import logging
import os

BOUNTY_CONTAINER_NAME = 'bounty'
CRIME_CONTAINER_NAME = 'crime'

logging.basicConfig(level=logging.INFO)

def main():

    blob_account_url = os.getenv('BLOB_ACCOUNT_URL')

    credentials = AzureCliCredential()
    blob_service_client = BlobServiceClient(account_url=blob_account_url,credential=credentials)

    container_bounty = blob_service_client.get_container_client(BOUNTY_CONTAINER_NAME)
    container_crime = blob_service_client.get_container_client(CRIME_CONTAINER_NAME)

    create_container(container_bounty)
    create_container(container_crime)
    

    logging.info(f"Validating if knowledge base is present")

def create_container(client:ContainerClient):
    if client.exists():
        client.delete_container()
    else:
        client.create_container()

def uploading_documents(client:ContainerClient,directory:str):
    files = os.listdir(directory)
    for file in files:
        logging.info(f"Processing file {file}")

if __name__ == "__main__":
    main()
