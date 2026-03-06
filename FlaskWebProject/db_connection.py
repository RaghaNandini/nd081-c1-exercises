from sqlalchemy import create_engine, text  # ✅ Import text
import urllib

# SQL Server credentials
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER = "cmsadmin"
SQL_PASSWORD = "Nandini@1"

# ODBC connection string
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

# Create engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Test connection
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            # ✅ Wrap SQL query with text()
            result = conn.execute(text("SELECT 1"))
            print("✅ DB Connected! Result:", result.scalar())
    except Exception as e:
        print("❌ Connection Failed:", e)