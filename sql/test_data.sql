
-- TESTOVACÍ DATA – SQL



IF NOT EXISTS (SELECT 1 FROM Position)
BEGIN
    INSERT INTO Position (name) VALUES
    ('GK'),
    ('DEF'),
    ('MID'),
    ('ATT');
END


INSERT INTO Team (name, league) VALUES
('Viktoria Plzeò', '1. LIGA'),
('Sigma Olomouc', '1. LIGA'),
('Zbrojovka Brno', '2. LIGA');


INSERT INTO Player (name, birth_date, height, active) VALUES
('Tomáš Koneèný', '1996-04-18', 1.82, 1),
('Lukáš Marek',   '1999-09-03', 1.76, 1),
('David Horák',   '2001-01-22', 1.88, 1),
('Filip Urban',   '1997-07-11', 1.74, 1),
('Ondøej Dvoøák', '1995-12-30', 1.90, 0);


INSERT INTO Contract (salary, type, valid_from, valid_to) VALUES
(85000,  'PROFESSIONAL', '2023-07-01', '2026-06-30'),
(42000,  'PROFESSIONAL', '2024-01-01', '2025-12-31'),
(15000,  'AMATEUR',     '2023-03-01', '2024-02-28'),
(30000,  'LOAN',        '2024-07-01', '2025-06-30');


INSERT INTO PlayerTeam (player_id, team_id, position_id, minutes_played) VALUES
(
    (SELECT id FROM Player WHERE name = 'Tomáš Koneèný'),
    (SELECT id FROM Team WHERE name = 'Viktoria Plzeò'),
    (SELECT id FROM Position WHERE name = 'DEF'),
    1850
),
(
    (SELECT id FROM Player WHERE name = 'Lukáš Marek'),
    (SELECT id FROM Team WHERE name = 'Viktoria Plzeò'),
    (SELECT id FROM Position WHERE name = 'MID'),
    1420
),
(
    (SELECT id FROM Player WHERE name = 'David Horák'),
    (SELECT id FROM Team WHERE name = 'Sigma Olomouc'),
    (SELECT id FROM Position WHERE name = 'ATT'),
    980
),
(
    (SELECT id FROM Player WHERE name = 'Filip Urban'),
    (SELECT id FROM Team WHERE name = 'Zbrojovka Brno'),
    (SELECT id FROM Position WHERE name = 'GK'),
    2100
);


INSERT INTO PlayerContract (player_id, contract_id) VALUES
(
    (SELECT id FROM Player WHERE name = 'Tomáš Koneèný'),
    (SELECT id FROM Contract WHERE salary = 85000)
),
(
    (SELECT id FROM Player WHERE name = 'Lukáš Marek'),
    (SELECT id FROM Contract WHERE salary = 42000)
),
(
    (SELECT id FROM Player WHERE name = 'David Horák'),
    (SELECT id FROM Contract WHERE salary = 15000)
),
(
    (SELECT id FROM Player WHERE name = 'Filip Urban'),
    (SELECT id FROM Contract WHERE type = 'LOAN')
);
