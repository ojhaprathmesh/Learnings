CREATE DATABASE IF NOT EXISTS students;
USE students;

SET autocommit = 0;

CREATE TABLE IF NOT EXISTS subjects (
    subjectID INT AUTO_INCREMENT PRIMARY KEY,
    subjectName VARCHAR(50) NOT NULL,
    courseName VARCHAR(50)
);

INSERT INTO subjects (subjectName, courseName)
VALUES 
("Maths", "B.Tech"),
("Chemistry", "B.Tech"),
("Business", "MBA"),
("Physcology", "Liberal Studies");

SELECT 
    *
FROM
    subjects;

SAVEPOINT SAVE1;

INSERT INTO subjects (subjectName, courseName)
VALUES 
("Hindi", "Literature"),
("English", "Literature"),
("Biology", "B.SC"),
("Philoshpy", "Liberal Studies");

SAVEPOINT SAVE2;

INSERT INTO subjects (subjectName, courseName)
VALUES 
("Maths", "B.Tech"),
("Chemistry", "B.Tech"),
("Business", "MBA"),
("Physcology", "Liberal Studies");

ROLLBACK TO SAVE2;

SELECT 
    *
FROM
    subjects;

USE imdb;

ALTER TABLE names RENAME TO directors;
ALTER TABLE director_mapping CHANGE name_id director_id VARCHAR(10);
ALTER TABLE directors CHANGE id director_id VARCHAR(10);
ALTER TABLE movie CHANGE id movie_id VARCHAR(10);

SELECT 
    m.*, d.*, dm.*
FROM
    directors d,
    director_mapping dm,
    movie m;

DELIMITER $$

CREATE PROCEDURE GetMoviesByLanguageAndDirector(
    IN lang VARCHAR(50), 
    IN director_name VARCHAR(100)
)
BEGIN
    SELECT 
        m.title, 
        d.name,
        m.languages,
        COUNT(m.movie_id) AS 'Movie Count'
    FROM
        movie m
        INNER JOIN director_mapping dm ON dm.movie_id = m.movie_id
        INNER JOIN directors d ON d.director_id = dm.director_id
    WHERE
        m.languages = lang
        OR d.name = director_name
    GROUP BY m.title, d.name, m.languages;
END $$

DELIMITER ;

CALL GetMoviesByLanguageAndDirector('German', 'Lauren Bacall');
