import csv
import json
from datetime import datetime
from src.models.Player import Player
from src.models.Team import Team
from src.dao.PlayerDAO import PlayerDAO
from src.dao.TeamDAO import TeamDAO


def import_players_from_csv(db, filename):
    player_dao = PlayerDAO(db)
    imported = 0

    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            header = f.readline()

            delimiter = ';' if ';' in header else ','

            f.seek(0)
            reader = csv.DictReader(f, delimiter=delimiter)

            for row in reader:
                player = Player(
                    name=row['name'].strip(),
                    birth_date=datetime.strptime(
                        row['birth_date'], '%d.%m.%Y'
                    ).date(),
                    height=float(row['height']),
                    active=row['active'] in ('1', 'true', 'True')
                )

                player_dao.create(player)
                imported += 1

        print(f"Importováno {imported} hráčů z CSV")

    except Exception as e:
        print(f"Chyba při importu CSV: {e}")
        raise



def import_teams_from_json(db, filename):
    team_dao = TeamDAO(db)
    imported = 0

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                team = Team(
                    name=item['name'],
                    league=item['league']
                )
                team_dao.create(team)
                imported += 1

        print(f"Importováno {imported} týmů z JSON")
    except Exception as e:
        print(f"Chyba při importu JSON: {e}")
        raise