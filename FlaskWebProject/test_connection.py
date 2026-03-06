from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv

# Load environment variables from your new.env
load_dotenv("new.env")
'''
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
'''
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER = "cmsadmin"
SQL_PASSWORD = "Nandini@1"

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
#engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Test connection
'''
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print(f"✅ Connected to SQL Server '{SQL_DATABASE}' successfully!")
    except Exception as e:
        print("❌ Connection failed:", e)'''
'''
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
print("DB connected:", result.scalar())'''

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Connected to DB, test query result:", result.scalar())
    except Exception as e:
        print("❌ Connection failed:", e)