# db.py
import os
import urllib
from sqlalchemy import create_engine

# Read environment variables from Azure App Service
server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USER_NAME")
password = os.environ.get("SQL_PASSWORD")

# Build connection string for Azure SQL
params = urllib.parse.quote_plus(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Uid={username};"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Create SQLAlchemy engine
<<<<<<< HEAD
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
=======
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
>>>>>>> f5f8fba (Fix Azure SQL connection)
