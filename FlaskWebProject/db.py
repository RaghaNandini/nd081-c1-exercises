# db.py
'''
from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv
'''
# Load .env
'''
load_dotenv() ''' # Make sure your .env or new.env exists
'''
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
'''

# db.py
'''
from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv
'''
# Load environment variables from new.env
'''
load_dotenv("new.env")
'''
# Get SQL credentials from environment
'''
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
'''

# Build connection string for ODBC Driver 18
'''
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)'''

# Create SQLAlchemy engine
#engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", echo=True)

# Optional: test connection
'''
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print(f"Successfully connected to {SQL_DATABASE} on {SQL_SERVER}")
            print("✅ Connection to SQL Server successful!")
    except Exception as e:
        print("Error connecting to database:", e)
        print("❌ Connection failed:", e)
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ Connection to SQL Server successful!")
    except Exception as e:
        print("❌ Connection failed:", e)'''
'''
# db.py
from sqlalchemy import create_engine
import urllib
import os

SQL_SERVER = os.environ.get("SQL_SERVER")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"  # Change to yes for Azure
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")'''
'''
# db.py
from sqlalchemy import create_engine, text
import os
import urllib

# Step 1: Read environment variables set in Azure
SQL_SERVER = os.environ.get("SQL_SERVER")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

# Step 2: Build connection string for SQL Server
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

# Step 3: Create SQLAlchemy engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Step 4: Function to get all users from the database
def get_all_users():
    with engine.connect() as conn:
        # Wrap SQL string in text()
        result = conn.execute(text("SELECT * FROM users"))
        # Fetch all rows
        rows = result.fetchall()
        # Convert to list of dicts for easier use
        users = [dict(row._mapping) for row in rows]
        return users

# Step 5: Optional test if running db.py directly
if __name__ == "__main__":
    users = get_all_users()
    for user in users:
        print(user)
'''
'''
# db.py in FlaskWebProject
from sqlalchemy import create_engine, text
import urllib
import os
from dotenv import load_dotenv

# Step 1: Load environment variables from new.env file (for local testing)
load_dotenv("new.env")

# Step 2: Fetch environment variables
SQL_SERVER = os.environ.get("SQL_SERVER")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
SQL_USER = os.environ.get("SQL_USER")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

# Step 3: Build connection string safely
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

# Step 4: Create SQLAlchemy engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
'''# db.py
from sqlalchemy import create_engine
import urllib
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv("new.env")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Build connection string using ODBC 18 (Azure recommended)
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"  # must be yes for local dev
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Test connection
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Connected to SQL Server:", result.scalar())
    except Exception as e:
        print("❌ Connection failed:", e)