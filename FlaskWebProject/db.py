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
    f"SERVER=tcp:{config.SQL_SERVER},1433;"
    f"Database={database};"
    f"Uid={username};"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Create SQLAlchemy engine

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

