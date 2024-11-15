import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from azure.storage.blob import BlobServiceClient, ContentSettings
import os

# Set up Azure Storage credentials and BlobServiceClient
p_account_name = 'unav0storage'#'YOUR_ACCOUNT_NAME'
p_account_key = '3Bi1lEI41WFNwv0mGfljs7HjRDuDuPN7nonIvqE8LfBGRSnbxRsDVYuCyJ2GhGk4qE5jwCmmQGu5+AStc2ZjOA=='#'YOUR_ACCOUNT_KEY'
blob_service_client = BlobServiceClient(account_url=f"https://{p_account_name}.blob.core.windows.net", credential=p_account_key)

def blob_to_container(container_name, file_name):
    # Get a client for the container
    container_client = blob_service_client.get_container_client(container_name)
    
    # Upload the blob
    with open(file_name, "rb") as data:
        container_client.upload_blob(
            name=file_name, 
            data=data,
            overwrite=True,  # Overwrite the blob if it already exists
            content_settings=ContentSettings(content_type='text/csv')
        )
    print(f"{file_name} uploaded to container {container_name} successfully.")

# Extract data from the web page and process it
url = 'https://servicios.ine.es/wstempus/js/ES/SERIES_TABLA/2852?page=1'
r = requests.get(url)
data = r.json()

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
file_name = 'pruebas.csv'
df.to_csv(file_name, header=False, sep=',', encoding='utf-8', index=False)

# Specify the container name and upload the CSV to Azure Blob Storage
container_name = 'landing'  # Ensure this is the container name only
blob_to_container(container_name=container_name, file_name=file_name)

# Optional: Clean up the temporary file
os.remove(file_name)