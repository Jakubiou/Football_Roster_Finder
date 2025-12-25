from db_connection import get_connection


class TeamDAO:

    def get_roster(self, team_name: str):
        if not team_name:
            return []

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT 
            Player,
            Position,
            ContractType,
            Minutes
        FROM V_TeamRoster
        WHERE Team = ? AND Minutes > 0
        """

        cursor.execute(sql, team_name)

        players = []
        for row in cursor.fetchall():
            players.append({
                "player": row.Player,
                "position": row.Position,
                "contract": row.ContractType,
                "minutes": row.Minutes
            })

        conn.close()
        return players
