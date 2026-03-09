
    
'''
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    # -------------------------------
    # Azure Blob Storage
    # -------------------------------
    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'ENTER_STORAGE_ACCOUNT_NAME'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'ENTER_BLOB_STORAGE_KEY'
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'ENTER_IMAGES_CONTAINER_NAME'

    # -------------------------------
    # Azure SQL Database
    # -------------------------------
    SQL_SERVER = os.environ.get('SQL_SERVER') or 'ENTER_SQL_SERVER_NAME.database.windows.net'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'ENTER_SQL_DB_NAME'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'ENTER_SQL_SERVER_USERNAME'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'ENTER_SQL_SERVER_PASSWORD'

    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://'
        + SQL_USER_NAME + ':' + SQL_PASSWORD
        + '@' + SQL_SERVER + ':1433/'
        + SQL_DATABASE
        + '?driver=ODBC+Driver+17+for+SQL+Server'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------
    # Microsoft Authentication
    # -------------------------------

    CLIENT_ID = "d7358fb4-d14d-4192-a8b5-cc1c8f83f74b"

    CLIENT_SECRET = "eP38Q~G4td2T5_vcgFoshpBU2PBN~NmHT4CpKbz~"

    TENANT_ID = "99e3203e-83c3-4b72-bd60-6b1d7166531a"

    AUTHORITY = "https://login.microsoftonline.com/" + TENANT_ID

    REDIRECT_PATH = "/getAToken"

    SCOPE = ["User.Read"]

    SESSION_TYPE = "filesystem"
    '''
'''
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

'''
'''
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
'''


import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"

# -------------------------
# Flask Secret Key
# -------------------------
SECRET_KEY = "12c86a9188995eccb21f4e0dd39eb9dd4beba50903aa21c2"


# -------------------------
# Azure SQL Database
# -------------------------
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER_NAME = "cmsadmin"
SQL_PASSWORD = "Nandini@1"


# -------------------------
# Azure AD Authentication
# -------------------------
CLIENT_ID = "d7358fb4-d14d-4192-a8b5-cc1c8f83f74b"
CLIENT_SECRET = "eP38Q~G4td2T5_vcgFoshpBU2PBN~NmHT4CpKbz~"
TENANT_ID = "99e3203e-83c3-4b72-bd60-6b1d7166531a"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

REDIRECT_PATH = "/getAToken"

SCOPE = ["User.Read"]


# -------------------------
# Azure Blob Storage
# -------------------------
BLOB_ACCOUNT_NAME = "imgcms12"

BLOB_ACCOUNT_KEY = "RjazZTzYJR9Li9Yos3/HLm1AkVqhcv3SC1EzI6Qdlo9X/w6/HEIpiasff3s4wN5dPbYDnPbSVRtz+AStu/mU5Q=="

BLOB_CONTAINER = "images"

BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=imgcms12;AccountKey=RjazZTzYJR9Li9Yos3/HLm1AkVqhcv3SC1EzI6Qdlo9X/w6/HEIpiasff3s4wN5dPbYDnPbSVRtz+AStu/mU5Q==;EndpointSuffix=core.windows.net"