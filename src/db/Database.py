import json
import pyodbc
import os


class Database:

    def __init__(self, config_path="config.json"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config soubor '{config_path}' nenalezen")

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.conn_str = config.get("connectionString")
        if not self.conn_str:
            raise KeyError("Missing 'connectionString' in config.json")

        self.connection = None
        self.cursor = None

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

    def execute(self, sql, *params):
        if not self.cursor:
            return
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
        except pyodbc.Error as e:
            if "does not exist" not in str(e).lower():
                print(f"SQL varování: {e}")

    def fetchall(self, sql, *params):
        if not self.cursor:
            return []
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"SQL chyba: {e}")
            return []

    def fetchone(self, sql, *params):
        if not self.cursor:
            return None
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except pyodbc.Error:
            return None

    def commit(self):
        if self.connection:
            self.connection.commit()

    def begin(self):
        if self.connection:
            self.connection.autocommit = False

    def rollback(self):
        if self.connection:
            self.connection.rollback()