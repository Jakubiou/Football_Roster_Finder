import pyodbc
from src.db.db_exceptions import ConfigError, DatabaseConnectionError
from src.lib.config_loader import load_config


class Database:

    def __init__(self, config_path="config.json"):
        config = load_config(config_path)

        self.conn_str = config.get("connectionString")
        if not self.conn_str:
            raise ConfigError(
                "V config.json chybí položka 'connectionString'."
            )

        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
        except pyodbc.Error:
            raise DatabaseConnectionError(
                "Nepodařilo se připojit k databázi.\n"
                "Zkontrolujte přihlašovací údaje a dostupnost serveru."
            )

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