from src.models.Contract import Contract


class ContractDAO:
    '''
    Data Access Object for managing Contract records in the database.
    Provides methods for CRUD operations (Create, Read, Update, Delete).
    '''

    def __init__(self, db):
        self.db = db

    def create(self, contract):
        '''
        Inserts a new contract record into the database.
        :param contract: An instance of the Contract model containing the data to be stored.
        :return: The unique ID (primary key) of the newly created contract, or None if failed.
        '''

        sql = """
        INSERT INTO Contract (salary, type, valid_from, valid_to)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(sql, contract.salary, contract.type, contract.valid_from, contract.valid_to)
        self.db.commit()

        result = self.db.fetchone("SELECT @@IDENTITY")
        return int(result[0]) if result else None

    def get_by_id(self, contract_id):
        '''
        Retrieves a contract record from the database.
        :param contract_id: The ID of the contract to retrieve.
        :return: A Contract object if found, otherwise None.
        '''

        sql = "SELECT id, salary, type, valid_from, valid_to FROM Contract WHERE id = ?"
        row = self.db.fetchone(sql, contract_id)
        if row:
            return Contract(row[0], row[1], row[2], row[3], row[4])
        return None

    def get_all(self):
        '''
        Retrieves all contract records from the database.
        :return: A list of all Contract objects present in the database.
        '''

        sql = "SELECT id, salary, type, valid_from, valid_to FROM Contract"
        rows = self.db.fetchall(sql)
        return [Contract(r[0], r[1], r[2], r[3], r[4]) for r in rows]

    def update(self, contract):
        '''
        Updates a contract record from the database.
        :param contract: The Contract object containing the updated information.
        :return: None
        '''

        sql = """
        UPDATE Contract
        SET salary = ?, type = ?, valid_from = ?, valid_to = ?
        WHERE id = ?
        """
        self.db.execute(sql, contract.salary, contract.type, contract.valid_from, contract.valid_to, contract.id)
        self.db.commit()

    def delete(self, contract_id):
        '''
        Deletes a contract record from the database.
        :param contract_id: The unique ID of the contract to be removed.
        :return: None
        '''
        sql = "DELETE FROM Contract WHERE id = ?"
        self.db.execute(sql, contract_id)
        self.db.commit()
