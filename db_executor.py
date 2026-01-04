import pyodbc
from config import DB_CONNECTION_STRING

def execute_query(sql: str):
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()

    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]
