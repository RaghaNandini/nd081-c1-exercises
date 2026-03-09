import os

# -------------------------
# Flask Secret Key
# -------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")

# -------------------------
# Azure SQL Database
# -------------------------
SQL_SERVER = os.environ.get("SQL_SERVER")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
SQL_USER_NAME = os.environ.get("SQL_USER_NAME")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

SQLALCHEMY_DATABASE_URI = (
    f"mssql+pyodbc://{SQL_USER_NAME}:{SQL_PASSWORD}"
    f"@{SQL_SERVER}:1433/{SQL_DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# -------------------------
# Azure AD Authentication
# -------------------------
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read"]

# -------------------------
# Azure Blob Storage
# -------------------------
BLOB_CONNECTION_STRING = os.environ.get("BLOB_CONNECTION_STRING")
BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")
