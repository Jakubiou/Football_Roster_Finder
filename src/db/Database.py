import pyodbc
from src.db.db_exceptions import ConfigError, DatabaseConnectionError
from src.lib.config_loader import load_config


class Database:
    '''
    Database class for managing Contract records in the database.
    '''

    def __init__(self, config_path="config.json"):
        '''
        Initializes the Database instance by loading configuration from a JSON file.
        :param config_path: Path to the configuration file containing the connection string.
        '''
        config = load_config(config_path)

        self.conn_str = config.get("connectionString")
        if not self.conn_str:
            raise ConfigError(
                "V config.json chybí položka 'connectionString'."
            )

        self.connection = None
        self.cursor = None

    def connect(self):
        '''
        Connects to the database using the connection string.
        :return: None
        '''
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
        except pyodbc.Error:
            raise DatabaseConnectionError(
                "Nepodařilo se připojit k databázi.\n"
                "Zkontrolujte přihlašovací údaje a dostupnost serveru."
            )

    def disconnect(self):
        '''
        Disconnects from the database using the connection string.
        :return: None
        '''
        try:
            if self.cursor:
                self.cursor.close()
        except:
            pass
        finally:
            try:
                if self.connection:
                    self.connection.close()
            except:
                pass

    def execute(self, sql, *params):
        '''
        Executes a query on the database using the connection string.
        :param sql: SQL query to execute.
        :param params: Parameters to pass to the query.
        :return: None 
        '''''
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
        '''
        Executes a query on the database using the connection string.
        :param sql: SQL query to execute.
        :param params: Parameters to pass to the query.
        :return: A list of all rows fetched from the query, or an empty list if failed.
        '''
        if not self.cursor:
            return []
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"SQL chyba: {e}")
            return []

    def fetchone(self, sql, *params):
        '''
        Executes a query on the database using the connection string.
        :param sql: SQL query to execute.
        :param params: Parameters to pass to the query.
        :return: The first row fetched from the query result, or None if no result or failed.
        '''
        if not self.cursor:
            return None
        try:
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        except pyodbc.Error:
            return None

    def commit(self):
        '''
        Commits to the database using the connection string.
        :return: None
        '''
        if self.connection:
            self.connection.commit()

    def begin(self):
        '''
        Begins the database transaction.
        :return: None
        '''
        if self.connection:
            self.connection.autocommit = False

    def rollback(self):
        '''
        Rolls back to the database transaction.
        :return: None
        '''
        if self.connection:
            self.connection.rollback()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()