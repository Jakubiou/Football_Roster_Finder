from src.models.Position import Position

class PositionDAO:

    def __init__(self, db):
        self.db = db

    def create(self, position):
        sql = "INSERT INTO Position (name) VALUES (?)"
        self.db.execute(sql, position.name)
        self.db.commit()

        row = self.db.fetchone("SELECT @@IDENTITY")
        return int(row[0])

    def get_all(self):
        sql = "SELECT id, name FROM Position"
        rows = self.db.fetchall(sql)
        return [Position(r[0], r[1]) for r in rows]

    def get_by_name(self, name):
        sql = "SELECT id, name FROM Position WHERE name = ?"
        r = self.db.fetchone(sql, name)
        return Position(r[0], r[1]) if r else None
