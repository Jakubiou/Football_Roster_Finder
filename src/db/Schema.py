def create_schema(db):

    print("Odstraňuji staré tabulky...")

    drop_statements = [
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

    print("Vytvářím tabulky...")

    create_tables = [
        """
        CREATE TABLE Team (
            id INT IDENTITY PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            league VARCHAR(20) NOT NULL CHECK (league IN ('1. LIGA', '2. LIGA')),
            founded_year INT,
            budget FLOAT
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
            code VARCHAR(10) NOT NULL CHECK (code IN ('GK', 'DEF', 'MID', 'ATT'))
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
        """
    ]

    for sql in create_tables:
        db.execute(sql)

    db.commit()
    print("Databázové tabulky vytvořeny")