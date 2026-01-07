from src.dao.PositionDAO import PositionDAO
from src.models.Position import Position


def ensure_schema(db):
    print("Kontrola databázové struktury")

    required_structure = {
        'Team': ['id', 'name', 'league'],
        'Player': ['id', 'name', 'birth_date', 'height', 'active'],
        'Position': ['id', 'name'],
        'Contract': ['id', 'salary', 'type', 'valid_from', 'valid_to'],
        'PlayerTeam': ['id', 'player_id', 'team_id', 'position_id', 'minutes_played'],
        'PlayerContract': ['player_id', 'contract_id']
    }

    required_views = ['V_TeamRoster', 'V_TeamStatistics']

    try:
        needs_recreation = False

        for table_name in required_structure.keys():
            table_exists = db.fetchone("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = ?
            """, table_name)

            if not table_exists:
                print(f"Tabulka '{table_name}' neexistuje")
                needs_recreation = True
                break

            expected_columns = set(required_structure[table_name])
            actual_columns_rows = db.fetchall("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = ?
            """, table_name)

            actual_columns = set(row[0].lower() for row in actual_columns_rows)
            expected_columns_lower = set(col.lower() for col in expected_columns)

            if actual_columns != expected_columns_lower:
                missing = expected_columns_lower - actual_columns
                extra = actual_columns - expected_columns_lower

                print(f"Tabulka '{table_name}' má špatnou strukturu:")
                if missing:
                    print(f"    Chybí sloupce: {', '.join(missing)}")
                if extra:
                    print(f"    Navíc sloupce: {', '.join(extra)}")

                needs_recreation = True
                break

        if not needs_recreation:
            for view_name in required_views:
                view_exists = db.fetchone("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.VIEWS 
                    WHERE TABLE_NAME = ?
                """, view_name)

                if not view_exists:
                    print(f"VIEW '{view_name}' neexistuje")
                    needs_recreation = True
                    break

        if needs_recreation:
            print("Databázová struktura je neplatná - provádím reinicializaci...")
            create_schema(db)
        else:
            print("Databázová struktura je v pořádku")

    except Exception as e:
        print(f"Chyba při kontrole schématu: {e}")
        print("Provádím automatickou inicializaci...")
        create_schema(db)


def create_schema(db):

    print("Odstraňuji FOREIGN KEY constrainty")

    drop_fks = """
    DECLARE @sql NVARCHAR(MAX) = N'';

    SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
        + '.' + QUOTENAME(OBJECT_NAME(parent_object_id))
        + ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
    FROM sys.foreign_keys;

    EXEC sp_executesql @sql;
    """

    try:
        db.execute(drop_fks)
        db.commit()
    except:
        pass

    print("Odstraňuji VIEW a tabulky")

    drop_statements = [
        "DROP VIEW IF EXISTS V_TeamStatistics",
        "DROP VIEW IF EXISTS V_TeamRoster",
        "DROP VIEW IF EXISTS V_CurrentRoster",
        "DROP VIEW IF EXISTS V_PlayerContracts",
        "DROP TABLE IF EXISTS PlayerContract",
        "DROP TABLE IF EXISTS PlayerTeam",
        "DROP TABLE IF EXISTS Contract",
        "DROP TABLE IF EXISTS Position",
        "DROP TABLE IF EXISTS Player",
        "DROP TABLE IF EXISTS Team"
    ]

    for sql in drop_statements:
        try:
            db.execute(sql)
        except:
            pass

    db.commit()

    print("Vytvářím tabulky")

    create_tables = [
        """
        CREATE TABLE Team (
            id INT IDENTITY PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            league VARCHAR(20) NOT NULL CHECK (league IN ('1. LIGA', '2. LIGA'))
        )
        """,

        """
        CREATE TABLE Player (
            id INT IDENTITY PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            birth_date DATE,
            height FLOAT,
            active BIT NOT NULL DEFAULT 1
        )
        """,

        """
        CREATE TABLE Position (
            id INT IDENTITY PRIMARY KEY,
            name VARCHAR(10) NOT NULL CHECK (name IN ('GK', 'DEF', 'MID', 'ATT'))
        )
        """,

        """
        CREATE TABLE Contract (
            id INT IDENTITY PRIMARY KEY,
            salary FLOAT NOT NULL,
            type VARCHAR(20) NOT NULL CHECK (type IN ('PROFESSIONAL', 'AMATEUR', 'LOAN')),
            valid_from DATE NOT NULL,
            valid_to DATE NOT NULL
        )
        """,

        """
        CREATE TABLE PlayerTeam (
            id INT IDENTITY PRIMARY KEY,
            player_id INT NOT NULL,
            team_id INT NOT NULL,
            position_id INT NOT NULL,
            minutes_played INT DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES Player(id),
            FOREIGN KEY (team_id) REFERENCES Team(id),
            FOREIGN KEY (position_id) REFERENCES Position(id)
        )
        """,

        """
        CREATE TABLE PlayerContract (
            player_id INT NOT NULL,
            contract_id INT NOT NULL,
            PRIMARY KEY (player_id, contract_id),
            FOREIGN KEY (player_id) REFERENCES Player(id),
            FOREIGN KEY (contract_id) REFERENCES Contract(id)
        )
        """
    ]

    for sql in create_tables:
        db.execute(sql)

    db.commit()

    print("Vytvářím VIEW")

    create_views = [
        """
        CREATE VIEW V_CurrentRoster AS
        SELECT
            t.name AS team,
            p.name AS player,
            pos.name AS position,
            pt.minutes_played
        FROM PlayerTeam pt
        JOIN Player p ON pt.player_id = p.id
        JOIN Team t ON pt.team_id = t.id
        JOIN Position pos ON pt.position_id = pos.id

        """,

        """
        CREATE VIEW V_PlayerContracts AS
        SELECT
            p.name AS player,
            c.type,
            c.salary,
            c.valid_from,
            c.valid_to
        FROM PlayerContract pc
        JOIN Player p ON pc.player_id = p.id
        JOIN Contract c ON pc.contract_id = c.id
        """,

        """
        CREATE VIEW V_TeamRoster AS
        SELECT
            t.name AS team,
            p.name AS player,
            pos.name AS position,
            pt.minutes_played AS minutes,
            p.height
        FROM PlayerTeam pt
        JOIN Player p ON pt.player_id = p.id
        JOIN Team t ON pt.team_id = t.id
        JOIN Position pos ON pt.position_id = pos.id
        WHERE p.active = 1 AND pt.minutes_played > 0
        """,

        """
        CREATE OR ALTER VIEW V_TeamStatistics AS
        SELECT
            t.name AS team,
            COUNT(pt.player_id) AS players,
            ISNULL(AVG(p.height), 0) AS avg_height,
            ISNULL(SUM(c.salary), 0) AS total_salary,
            ISNULL(SUM(pt.minutes_played), 0) AS total_minutes
        FROM Team t
        LEFT JOIN PlayerTeam pt ON t.id = pt.team_id
        LEFT JOIN Player p ON pt.player_id = p.id
        LEFT JOIN PlayerContract pc ON p.id = pc.player_id
        LEFT JOIN Contract c ON pc.contract_id = c.id
        GROUP BY t.name

        """
    ]

    pos_dao = PositionDAO(db)

    for code in ["GK", "DEF", "MID", "ATT"]:
        pos_dao.create(Position(name=code))

    print("Výchozí pozice vytvořeny")

    for sql in create_views:
        db.execute(sql)

    db.commit()

    print("Databáze úspěšně vytvořena!")