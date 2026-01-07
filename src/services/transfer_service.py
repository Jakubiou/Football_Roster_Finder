def transfer_player(db, player_id, from_team_id, to_team_id, new_position_id, new_contract_id):
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
