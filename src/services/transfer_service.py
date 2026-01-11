def transfer_player(db, player_id, from_team_id, to_team_id, new_position_id, new_contract_id):
    '''
    Executes a player transfer between two teams as a single database transaction.
    This process removes the player from the old team, assigns them to the new team
    with a starting value of 0 minutes played, and links them to a new contract.
    :param db: The database connection instance supporting transaction methods (begin, commit, rollback).
    :param player_id: The unique ID of the player being transferred.
    :param from_team_id: The unique ID of the source team (from which the player is leaving).
    :param to_team_id: The unique ID of the target team (which the player is joining).
    :param new_position_id: The unique ID of the position assigned to the player in the new team.
    :param new_contract_id: The unique ID of the contract to be associated with the player.
    :raises Exception: If any part of the transaction fails, a rollback is performed and the error is re-raised.
    :return: None
    '''
    try:
        db.begin()
        db.execute(
            "DELETE FROM PlayerTeam WHERE player_id = ? AND team_id = ?",
            player_id, from_team_id
        )

        db.execute("""
            INSERT INTO PlayerTeam (player_id, team_id, position_id, minutes_played)
            VALUES (?, ?, ?, 0)
        """, player_id, to_team_id, new_position_id)

        db.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM PlayerContract
                WHERE player_id = ? AND contract_id = ?
            )
            BEGIN
                INSERT INTO PlayerContract (player_id, contract_id)
                VALUES (?, ?)
            END
        """, player_id, new_contract_id, player_id, new_contract_id)

        db.commit()

    except Exception as e:
        db.rollback()
        raise
