CREATE TABLE Team (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    league VARCHAR(20) NOT NULL
        CHECK (league IN ('1. LIGA', '2. LIGA'))
);
GO

CREATE TABLE Player (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    height FLOAT,
    active BIT NOT NULL DEFAULT 1
);
GO

CREATE TABLE Position (
    id INT IDENTITY PRIMARY KEY,
    name VARCHAR(10) NOT NULL
        CHECK (name IN ('GK', 'DEF', 'MID', 'ATT'))
);
GO

CREATE TABLE Contract (
    id INT IDENTITY PRIMARY KEY,
    salary FLOAT NOT NULL,
    type VARCHAR(20) NOT NULL
        CHECK (type IN ('PROFESSIONAL', 'AMATEUR', 'LOAN')),
    valid_from DATE NOT NULL,
    valid_to DATE NOT NULL
);
GO

CREATE TABLE PlayerTeam (
    id INT IDENTITY PRIMARY KEY,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    position_id INT NOT NULL,
    minutes_played INT DEFAULT 0,
    CONSTRAINT FK_PlayerTeam_Player
        FOREIGN KEY (player_id) REFERENCES Player(id),
    CONSTRAINT FK_PlayerTeam_Team
        FOREIGN KEY (team_id) REFERENCES Team(id),
    CONSTRAINT FK_PlayerTeam_Position
        FOREIGN KEY (position_id) REFERENCES Position(id)
);
GO

CREATE TABLE PlayerContract (
    player_id INT NOT NULL,
    contract_id INT NOT NULL,
    CONSTRAINT PK_PlayerContract PRIMARY KEY (player_id, contract_id),
    CONSTRAINT FK_PlayerContract_Player
        FOREIGN KEY (player_id) REFERENCES Player(id),
    CONSTRAINT FK_PlayerContract_Contract
        FOREIGN KEY (contract_id) REFERENCES Contract(id)
);
GO



CREATE VIEW V_CurrentRoster AS
SELECT
    t.name AS team,
    p.name AS player,
    pos.name AS position,
    pt.minutes_played
FROM PlayerTeam pt
JOIN Player p ON pt.player_id = p.id
JOIN Team t ON pt.team_id = t.id
JOIN Position pos ON pt.position_id = pos.id;
GO


CREATE VIEW V_PlayerContracts AS
SELECT
    p.name AS player,
    c.type,
    c.salary,
    c.valid_from,
    c.valid_to
FROM PlayerContract pc
JOIN Player p ON pc.player_id = p.id
JOIN Contract c ON pc.contract_id = c.id;
GO


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
WHERE p.active = 1
  AND pt.minutes_played > 0;
GO


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
GROUP BY t.name;
GO