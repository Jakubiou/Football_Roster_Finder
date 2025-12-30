import json
import pyodbc
import os
from typing import Optional


class Database:

    def __init__(self, config_path: str = "config.json"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config soubor '{config_path}' nenalezen")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.conn_str = config.get("connectionString")
        if not self.conn_str:
            raise KeyError("Missing 'connectionString' in config.json")

        self.connection: Optional[pyodbc.Connection] = None
        self.cursor: Optional[pyodbc.Cursor] = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
            print("Připojeno k databázi")
        except pyodbc.Error as e:
            print(f"Chyba připojení: {e}")
            raise

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Odpojeno od databáze")