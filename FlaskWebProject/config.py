
import os

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# -------------------------------
# Flask Secret Key
# -------------------------------
SECRET_KEY = "super_secret_flask_key"


# -------------------------------
# Azure SQL Database
# -------------------------------
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER_NAME = "cmsadmin"
SQL_PASSWORD = "Nandini@1"

SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://"
    + SQL_USER_NAME + ":" + SQL_PASSWORD
    + "@"
    + SQL_SERVER
    + ":1433/"
    + SQL_DATABASE
    + "?driver=ODBC+Driver+17+for+SQL+Server"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False


# -------------------------------
# Azure Blob Storage
# -------------------------------
BLOB_ACCOUNT = "ENTER_STORAGE_ACCOUNT_NAME"
BLOB_STORAGE_KEY = "ENTER_BLOB_STORAGE_KEY"
BLOB_CONTAINER = "ENTER_IMAGES_CONTAINER_NAME"


# -------------------------------
# Microsoft Authentication (Azure AD)
# -------------------------------

CLIENT_ID = "d7358fb4-d14d-4192-a8b5-cc1c8f83f74b"

CLIENT_SECRET = "eP38Q~G4td2T5_vcgFoshpBU2PBN~NmHT4CpKbz~"

TENANT_ID = "99e3203e-83c3-4b72-bd60-6b1d7166531a"

AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID

# Must match redirect URI in Azure Portal
REDIRECT_PATH = "/getAToken"

# Microsoft Graph permission
SCOPE = ["User.Read"]

# Session storage
SESSION_TYPE = "filesystem"