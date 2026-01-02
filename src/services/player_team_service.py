def add_player_to_team(db, player_id, team_id, position_id):
    sql = """
    INSERT INTO PlayerTeam (player_id, team_id, position_id, minutes_played)
    VALUES (?, ?, ?, 0)
    """
    db.execute(sql, player_id, team_id, position_id)
    db.commit()


def remove_player_from_team(db, player_id, team_id):
    sql = "DELETE FROM PlayerTeam WHERE player_id = ? AND team_id = ?"
    db.execute(sql, player_id, team_id)
    db.commit()


def update_minutes(db, player_id, team_id, minutes):
    db.execute("""
        UPDATE PlayerTeam
        SET minutes_played = minutes_played + ?
        WHERE player_id = ? AND team_id = ?
    """, minutes, player_id, team_id)
    db.commit()


def change_position(db, player_id, position_id):
    sql = """
    UPDATE PlayerTeam
    SET position_id = ?
    WHERE player_id = ?
    """
    db.execute(sql, position_id, player_id)
    db.commit()


def create_contract(db, salary, ctype, valid_from, valid_to):
    sql = """
    INSERT INTO Contract (salary, type, valid_from, valid_to)
    VALUES (?, ?, ?, ?)
    """
    db.execute(sql, salary, ctype, valid_from, valid_to)
    db.commit()
    result = db.fetchone("SELECT @@IDENTITY")
    return int(result[0]) if result else None


def assign_contract_to_player(db, player_id, contract_id):
    sql = "INSERT INTO PlayerContract (player_id, contract_id) VALUES (?, ?)"
    db.execute(sql, player_id, contract_id)
    db.commit()
