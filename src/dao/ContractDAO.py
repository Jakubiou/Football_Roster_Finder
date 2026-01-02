from src.models.Contract import Contract


class ContractDAO:

    def __init__(self, db):
        self.db = db

    def create(self, contract):
        sql = """
        INSERT INTO Contract (salary, type, valid_from, valid_to)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(sql, contract.salary, contract.type, contract.valid_from, contract.valid_to)
        self.db.commit()

        result = self.db.fetchone("SELECT @@IDENTITY")
        return int(result[0]) if result else None

    def get_by_id(self, contract_id):
        sql = "SELECT id, salary, type, valid_from, valid_to FROM Contract WHERE id = ?"
        row = self.db.fetchone(sql, contract_id)
        if row:
            return Contract(row[0], row[1], row[2], row[3], row[4])
        return None

    def get_all(self):
        sql = "SELECT id, salary, type, valid_from, valid_to FROM Contract"
        rows = self.db.fetchall(sql)
        return [Contract(r[0], r[1], r[2], r[3], r[4]) for r in rows]

    def update(self, contract):
        sql = """
        UPDATE Contract
        SET salary = ?, type = ?, valid_from = ?, valid_to = ?
        WHERE id = ?
        """
        self.db.execute(sql, contract.salary, contract.type, contract.valid_from, contract.valid_to, contract.id)
        self.db.commit()

    def delete(self, contract_id):
        sql = "DELETE FROM Contract WHERE id = ?"
        self.db.execute(sql, contract_id)
        self.db.commit()
