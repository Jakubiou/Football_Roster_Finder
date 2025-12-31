from src.models.Player import Player


class PlayerDAO:

    def __init__(self, db):
        self.db = db

    def create(self, player):
        sql = """
        INSERT INTO Player (name, birth_date, height, active)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(sql, player.name, player.birth_date, player.height, player.active)
        self.db.commit()

        result = self.db.fetchone("SELECT @@IDENTITY")
        return int(result[0]) if result else None

    def get_by_id(self, player_id):
        sql = "SELECT id, name, birth_date, height, active FROM Player WHERE id = ?"
        row = self.db.fetchone(sql, player_id)

        if row:
            return Player(row[0], row[1], row[2], row[3], bool(row[4]))
        return None

    def get_all(self):
        sql = "SELECT id, name, birth_date, height, active FROM Player"
        rows = self.db.fetchall(sql)

        return [Player(r[0], r[1], r[2], r[3], bool(r[4])) for r in rows]

    def update(self, player):
        sql = """
        UPDATE Player
        SET name = ?, birth_date = ?, height = ?, active = ?
        WHERE id = ?
        """
        self.db.execute(sql, player.name, player.birth_date, player.height,
                        player.active, player.id)
        self.db.commit()

    def delete(self, player_id):
        sql = "DELETE FROM Player WHERE id = ?"
        self.db.execute(sql, player_id)
        self.db.commit()