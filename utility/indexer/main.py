from dotenv import load_dotenv
import requests
import os
import json
import logging

logging.basicConfig(level=logging.INFO)

def main():
    load_dotenv(override=True)

    search_endpoint = os.getenv('SEARCH_ENDPOINT')
    search_api_key = os.getenv('SEARCH_API_KEY')
    search_api_version = os.getenv('SEARCH_API_VERSION')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    index_file_path = os.path.join(project_root, 'index', 'indexes.json')

    with open(index_file_path, 'r') as file:
        indexes = json.load(file)    

    headers = {
        'Content-Type': 'application/json',
        'api-key': search_api_key
    }
    
    for idx in indexes:
        
        # First we delete existing index
        url = f"{search_endpoint}/indexes('{idx['name']}')?api-version={search_api_version}"

        logging.info(f"Deleting index: {idx['name']}")

        requests.delete(url=url,headers=headers)

        logging.info(f"Creating/Updating index: {idx['name']}")

        url = f"{search_endpoint}/indexes('{idx['name']}')?api-version={search_api_version}"

        response = requests.put(url=url,headers=headers,data=json.dumps(idx))

        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:            
            logging.info(f"Status Code: {response.status_code}")
            logging.info("Index created/updated successfully")        
        else:
            logging.error(f"Error: {response.status_code}")
            logging.error(response.text)

if __name__ == "__main__":
    main()
