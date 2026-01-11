def generate_team_statistics(db):
    '''
    generates team statistics table
    :param db: The database connection instance.
    :return: None
    '''
    sql = """
    SELECT team, players, avg_height, total_salary, total_minutes
    FROM V_TeamStatistics
    ORDER BY players DESC
    """

    rows = db.fetchall(sql)

    return [
        {
            "team": r[0],
            "players": r[1] or 0,
            "avg_height": round(r[2] or 0, 2),
            "total_salary": r[3] or 0,
            "total_minutes": r[4] or 0
        }
        for r in rows
    ]
