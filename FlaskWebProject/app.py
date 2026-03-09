import logging
import urllib
from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient
from FlaskWebProject import config

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# Azure SQL Database
# -------------------------
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={config.SQL_SERVER};"
    f"DATABASE={config.SQL_DATABASE};"
    f"UID={config.SQL_USER_NAME};"
    f"PWD={config.SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    pool_pre_ping=True
)

# -------------------------
# Azure Blob Storage
# -------------------------
blob_service_client = BlobServiceClient.from_connection_string(
    config.BLOB_CONNECTION_STRING
)

blob_container_client = blob_service_client.get_container_client(
    config.BLOB_CONTAINER
<<<<<<< HEAD
)
=======
)
>>>>>>> 049acbd (Update project files and fix deployment)
