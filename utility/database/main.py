from azure.cosmos.cosmos_client import CosmosClient
from dotenv import load_dotenv
from collections import defaultdict
import azure.cosmos.exceptions as exceptions
import os
import json
import uuid
import logging

logging.basicConfig(level=logging.INFO)

def main():

    load_dotenv(override=True)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir,'data.json')

    with open(data_file_path,'r') as file:
        documents = json.load(file)

    COSMOS_DB_CNX_STRING = os.getenv('COSMOS_DB_CNX_STRING')
    DATABASE_ID = os.getenv('DATABASE_ID')
    CONTAINER_ID = os.getenv('CONTAINER_ID')
    PARTITION_KEY = os.getenv('PARTITION_KEY')

    cosmos_client = CosmosClient.from_connection_string(COSMOS_DB_CNX_STRING)
    db = cosmos_client.get_database_client(DATABASE_ID)
    container = db.get_container_client(CONTAINER_ID)

    batch_operation_documents = []

    # Group documents by partition key value
    docs_by_partition = defaultdict(list)

    for doc in documents:
        doc['id'] = str(uuid.uuid4())
        partition_value = doc[PARTITION_KEY]      
        docs_by_partition[partition_value].append(('create', (doc,)))
    
    for partition_value, batch_operations in docs_by_partition.items():
        try:
            container.execute_item_batch(batch_operations=batch_operations, partition_key=partition_value)
        except exceptions.CosmosBatchOperationError as e:
            error_operation_index = e.error_index
            error_operation_response = e.operation_responses[error_operation_index]
            error_operation = batch_operation_documents[error_operation_index]
            print("\nError operation: {}, error operation response: {}\n".format(error_operation, error_operation_response))
            print("\nAn error occurred in the batch operation. All operations have been rolled back.\n")        

if __name__ == "__main__":
    main()
