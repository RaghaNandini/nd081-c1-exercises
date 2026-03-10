import os

SECRET_KEY = os.environ.get("SECRET_KEY")

# SQL DATABASE
SQL_SERVER = os.environ.get("SQL_SERVER")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
SQL_USER_NAME = os.environ.get("SQL_USER_NAME")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

# BLOB STORAGE
BLOB_CONNECTION_STRING = os.environ.get("BLOB_CONNECTION_STRING")
BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")

# MICROSOFT LOGIN
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")
