import pyodbc
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def get_connection() -> pyodbc.Connection:
    conn_str = (
        f"DRIVER={{HFSQL}};"
        f"Server={os.getenv('HFSQL_SERVER')};"
        f"Port={os.getenv('HFSQL_PORT')};"
        f"Database={os.getenv('HFSQL_DATABASE')};"
        f"UID={os.getenv('HFSQL_USER')};"
        f"PWD={os.getenv('HFSQL_PASSWORD')};"
    )
    return pyodbc.connect(conn_str)


def listar_tablas() -> list[str]:
    with get_connection() as conn:
        cursor = conn.cursor()
        return [row.table_name for row in cursor.tables(tableType="TABLE")]
