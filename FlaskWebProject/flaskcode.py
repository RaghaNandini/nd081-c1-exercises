#Flask code for uploading/downloading blobs
from azure.storage.blob import BlobServiceClient
import os

# Load .env
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")

# Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER)

# Upload example
def upload_file(file_path, blob_name):
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"{blob_name} uploaded successfully!")

# Download example
def download_file(blob_name, download_path):
    with open(download_path, "wb") as file:
        file.write(container_client.download_blob(blob_name).readall())
    print(f"{blob_name} downloaded successfully!")