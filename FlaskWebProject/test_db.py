from sqlalchemy import create_engine, text
import urllib
import config

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={config.SQL_SERVER};"
    f"DATABASE={config.SQL_DATABASE};"
    f"UID={config.SQL_USER_NAME};"
    f"PWD={config.SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=30;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1 AS test"))
    for row in result:
        print(row)