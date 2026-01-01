from src.models.Team import Team


class TeamDAO:

    def __init__(self, db):
        self.db = db

    def create(self, team):
        sql = """
        INSERT INTO Team (name, league, founded_year, budget)
        VALUES (?, ?, ?, ?)
        """
        self.db.execute(sql, team.name, team.league, team.founded_year, team.budget)
        self.db.commit()

        result = self.db.fetchone("SELECT @@IDENTITY")
        return int(result[0]) if result else None

    def get_by_name(self, name):
        sql = "SELECT id, name, league, founded_year, budget FROM Team WHERE name = ?"
        row = self.db.fetchone(sql, name)

        if row:
            return Team(row[0], row[1], row[2], row[3], row[4])
        return None

    def get_all(self):
        sql = "SELECT id, name, league, founded_year, budget FROM Team"
        rows = self.db.fetchall(sql)

        return [Team(r[0], r[1], r[2] or "", r[3], r[4] or 0) for r in rows]

    def get_roster(self, team_name):
        sql = """
        SELECT Player, Position, ContractType, Minutes, Height
        FROM V_TeamRoster
        WHERE Team = ? AND Active = 1 AND Minutes > 0
        """
        rows = self.db.fetchall(sql, team_name)

        return [
            {
                "player": r[0],
                "position": r[1],
                "contract": r[2] if r[2] else "N/A",
                "minutes": r[3],
                "height": r[4]
            }
            for r in rows
        ]