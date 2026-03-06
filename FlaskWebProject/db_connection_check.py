# db_connection_check.py

from sqlalchemy import create_engine, text
import urllib

# --- SQL Server connection details ---
SQL_SERVER = "cms-sql-server.database.windows.net"
SQL_DATABASE = "cms"
SQL_USER = "cmsadmin"
SQL_PASSWORD = "Nandini@1"

# --- Build connection string ---
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

# --- Create engine ---
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", echo=False)

# --- Main function ---
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            # ✅ Wrap SQL string in text()
            result = conn.execute(
                text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
            )
            tables = [row[0] for row in result]

            if not tables:
                print("❌ No tables found in database!")
            else:
                print("✅ Tables in database:", tables)

            # --- Optional: Count rows for each table ---
            for table in tables:
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM [{table}]"))
                row_count = count_result.scalar()
                print(f"Table '{table}' has {row_count} rows.")

    except Exception as e:
        print("❌ Connection failed:", e)