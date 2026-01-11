def add_player_to_team(db, player_id, team_id, position_id):
    '''
    Adds a player to the team.
    :param db: The database connection instance.
    :param player_id: Id of the player to add.
    :param team_id: Id of the team to add.
    :param position_id: Id of the position to add.
    :return: None
    '''
    sql = """
    INSERT INTO PlayerTeam (player_id, team_id, position_id, minutes_played)
    VALUES (?, ?, ?, 0)
    """
    db.execute(sql, player_id, team_id, position_id)
    db.commit()


def remove_player_from_team(db, player_id, team_id):
    '''
    Removes a player from the team.
    :param db: The database connection instance.
    :param player_id: Id of the player to add.
    :param team_id: Id of the team to add.
    :return: None
    '''
    sql = "DELETE FROM PlayerTeam WHERE player_id = ? AND team_id = ?"
    db.execute(sql, player_id, team_id)
    db.commit()


def update_minutes(db, player_id, team_id, minutes):
    '''
    Updates the minutes played for the team.
    :param db: The database connection instance.
    :param player_id: Id of the player to add.
    :param team_id: Id of the team to add.
    :param minutes: New minutes played for the team.
    :return: None
    '''
    db.execute("""
        UPDATE PlayerTeam
        SET minutes_played = minutes_played + ?
        WHERE player_id = ? AND team_id = ?
    """, minutes, player_id, team_id)
    db.commit()


def change_position(db, player_id, position_id):
    '''
    Changes the position of the player.
    :param db: The database connection instance.
    :param player_id: Id of the player to add.
    :param position_id: Id of the position to add.
    :return: None
    '''
    sql = """
    UPDATE PlayerTeam
    SET position_id = ?
    WHERE player_id = ?
    """
    db.execute(sql, position_id, player_id)
    db.commit()


def create_contract(db, salary, ctype, valid_from, valid_to):
    '''
    Creates a contract for the player.
    :param db: The database connection instance.
    :param salary: The salary of the player.
    :param ctype: The type of the contract.
    :param valid_from: The date of the contract from which the player will start.
    :param valid_to: The date of the contract from which the player will start.
    :return: None
    '''
    sql = """
    INSERT INTO Contract (salary, type, valid_from, valid_to)
    VALUES (?, ?, ?, ?)
    """
    db.execute(sql, salary, ctype, valid_from, valid_to)
    db.commit()
    result = db.fetchone("SELECT @@IDENTITY")
    return int(result[0]) if result else None


def assign_contract_to_player(db, player_id, contract_id):
    '''
    Assigns a contract for the player.
    :param db: The database connection instance.
    :param player_id: Id of the player to add.
    :param contract_id: Id of the contract to add.
    :return: None
    '''
    sql = "INSERT INTO PlayerContract (player_id, contract_id) VALUES (?, ?)"
    db.execute(sql, player_id, contract_id)
    db.commit()
