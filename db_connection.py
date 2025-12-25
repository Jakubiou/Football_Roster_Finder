import json
import pyodbc


def get_connection():
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    conn_str = config["connectionString"]
    return pyodbc.connect(conn_str)
