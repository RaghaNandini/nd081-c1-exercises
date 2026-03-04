from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# SQL Database
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Blob Storage
BLOB_ACCOUNT = os.getenv("BLOB_ACCOUNT")
BLOB_ACCOUNT_KEY = os.getenv("BLOB_ACCOUNT_KEY")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")

# Microsoft Entra (Azure AD)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")