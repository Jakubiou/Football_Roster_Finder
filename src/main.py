from src.db.Database import Database
from src.db.Schema import create_schema
from src.dao.PlayerDAO import PlayerDAO
from src.dao.TeamDAO import TeamDAO
from src.models.Player import Player
from src.models.Team import Team
from datetime import date


def main():
    db = Database()

    try:
        db.connect()
        create_schema(db)

        team_dao = TeamDAO(db)

        team = Team(name="AC Sparta Praha", league="1. LIGA", founded_year=1893, budget=50000000)
        team_id = team_dao.create(team)
        print(team_id)

        all_teams = team_dao.get_all()
        print(len(all_teams))

        player_dao = PlayerDAO(db)

        player = Player(name="Ladislav Krejčí", birth_date=date(1999, 7, 5),
                        height=1.83, active=True)
        player_id = player_dao.create(player)
        print(player_id)

        loaded_player = player_dao.get_by_id(player_id)
        print(loaded_player)

        all_players = player_dao.get_all()
        print(len(all_players))


    except Exception as e:
        print(f"\n✗ Chyba: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()