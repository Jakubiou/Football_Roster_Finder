from src.models.Team import Team


class TeamDAO:

    def __init__(self, db):
        self.db = db

    def create(self, team):
        '''
        Creates a new team record in the database.
        :param team: Team to create.
        :return: None
        '''
        sql = """
        INSERT INTO Team (name, league)
        VALUES (?, ?)
        """
        self.db.execute(
            sql,
            team.name,
            team.league
        )
        self.db.commit()

        result = self.db.fetchone("SELECT SCOPE_IDENTITY()")
        return int(result[0]) if result and result[0] is not None else None

    def get_by_name(self, name):
        '''
        returns a team record by its name.
        :param name: Name of the Team.
        :return: name of team
        '''
        sql = """
        SELECT id, name, league, founded_year, budget
        FROM Team
        WHERE name = ?
        """
        row = self.db.fetchone(sql, name)

        if row:
            return Team(row[0], row[1], row[2])
        return None

    def get_all(self):
        '''
        returns a list of all team records.
        :return: list of teams
        '''
        sql = """
        SELECT id, name, league
        FROM Team
        """
        rows = self.db.fetchall(sql)

        return [
            Team(
                r[0],
                r[1],
                r[2] or "",
            )
            for r in rows
        ]

    def get_roster(self, team_name):
        '''
        returns a team record by its name.
        :param team_name: Name of the Team.
        :return: team record
        '''
        sql = """
        SELECT player, position, minutes, height
        FROM V_TeamRoster
        WHERE team = ?
        ORDER BY position, player
        """
        rows = self.db.fetchall(sql, team_name)

        return [
            {
                "player": r[0],
                "position": r[1],
                "minutes": r[2],
                "height": r[3]
            }
            for r in rows
        ]

    def get_players_in_team(self, team_id):
        '''
        returns a list of players record by its ID.
        :param team_id: ID of the Team.
        :return: list of players
        '''
        sql = """
        SELECT p.id, p.name
        FROM PlayerTeam pt
        JOIN Player p ON pt.player_id = p.id
        WHERE pt.team_id = ?
        """
        return self.db.fetchall(sql, team_id)
