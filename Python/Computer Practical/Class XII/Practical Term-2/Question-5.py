"""
Pr@thmesh2307
USE school;
SELECT * FROM dragonball;
SELECT * FROM raceinfo;
DROP TABLE dragonball, raceinfo;
CREATE TABLE `DragonBall`
(
Name varchar(25) PRIMARY KEY NOT NULL,
TotalForms int NOT NULL,
MaxForm varchar(25),
Gender varchar(10)
);
CREATE TABLE `RaceInfo`
(
Name varchar(25) PRIMARY KEY NOT NULL
);
DESC raceinfo;
ALTER TABLE raceinfo ADD (Race varchar(15));
DESC raceinfo;
INSERT INTO dragonball VALUES ('Goku', 10, 'Ultra Instinct Mastered', 'Male');
INSERT INTO dragonball VALUES ('Vegeta', 10, 'Ultra Ego', 'Male');
INSERT INTO dragonball VALUES ('Piccolo', 2, 'Super Namek', 'None');
INSERT INTO dragonball VALUES ('Majin Buu', 9, 'Uub', 'Male');
SELECT * FROM dragonball;
INSERT INTO raceinfo VALUES ('Goku', 'Saiyan');
INSERT INTO raceinfo VALUES ('Vegeta', 'Saiyan');
INSERT INTO raceinfo VALUES ('Majin Buu', 'Majin');
SELECT * FROM raceinfo;
SELECT * FROM dragonball;
UPDATE dragonball SET MaxForm = 'Mastered Ultra Instinct' WHERE Name = 'Goku';
SELECT * FROM dragonball;
DELETE FROM dragonball WHERE Gender = 'None';
SELECT * FROM dragonball;
SELECT * FROM dragonball ORDER BY MaxForm DESC;
SELECT * FROM dragonball WHERE MaxForm LIKE '%Ultra%';
SELECT * FROM dragonball db INNER JOIN raceinfo info ON db.Name = info.Name;
"""
"""
Join
"""