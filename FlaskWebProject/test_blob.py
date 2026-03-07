from azure.storage.blob import BlobServiceClient
import config

blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER)

with open("C:\\Users\\Ragha Nandini\\Downloads\\hello.png", "rb") as f:
    blob_client = blob_container_client.get_blob_client("test_upload.png")
    blob_client.upload_blob(f, overwrite=True)
    print("Uploaded successfully!")