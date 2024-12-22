USE imdb;
SET SQL_SAFE_UPDATES = 0;

-- Q1: Create a new table actor_mapping with columns actor_id and movie_id.
CREATE TABLE IF NOT EXISTS actor_mapping (
    actor_id VARCHAR(10) NOT NULL,
    movie_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (actor_id , movie_id)
);

-- Q2: Create a new table ratings with columns rating_id, movie_id, and rating.
CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id VARCHAR(10) NOT NULL,
    rating DECIMAL(3 , 2 )
);

-- Q3: Add a column budget to the movie table.
ALTER TABLE movie
ADD budget BIGINT;

-- Q4: Rename the column R_name in generic_records2 to record_name.
ALTER TABLE generic_records2
CHANGE R_name record_name VARCHAR(255);

-- Q5: Drop the table student.
DROP TABLE student;

-- Q6: Drop the table genre if it exists.
DROP TABLE IF EXISTS actor_mapping;

-- Q7: Insert a new movie into the movie table.
INSERT INTO movie (id, title, year, date_published, duration, country)
VALUES ('tt1234567', 'Sample Movie', 2024, '2024-11-01', 120, 'USA');

-- Q8: Insert a new person into the names table.
INSERT INTO names (id, name, height, date_of_birth)
VALUES ('nm1234567', 'John Doe', 180, '1985-07-15');

-- Q9: Update the duration of the movie with ID tt1234567 to 150 minutes.
UPDATE movie 
SET 
    duration = 150
WHERE
    id = 'tt1234567';

-- Q10: Update the category of generic_records2 with record_id = 1 to Updated Category.
UPDATE generic_records2 
SET 
    category = 'Updated Category'
WHERE
    record_id = 1;

-- Q11: Delete all records from the director_mapping table where movie_id is 'tt1234567'.
DELETE FROM director_mapping 
WHERE
    movie_id = 'tt1234567';

-- Q12: Delete records from names table where height is NULL.
DELETE FROM names 
WHERE
    height IS NULL;

SHOW GRANTS FOR CURRENT_USER;
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'password';

-- Q13: Grant all privileges on the imdb database to user john_doe (with GRANT OPTION).
GRANT ALL PRIVILEGES ON imdb.* TO 'root'@'localhost' WITH GRANT OPTION;

-- Q14: Grant INSERT, UPDATE, DELETE privileges on the names table to user john_doe.
GRANT INSERT, UPDATE, DELETE ON imdb.names TO 'root'@'localhost';

-- Q15: Revoke INSERT, UPDATE, DELETE privileges on the names table from user john_doe.
REVOKE INSERT, UPDATE, DELETE ON imdb.names FROM 'root'@'localhost';

-- Q16: Revoke ALL privileges on the imdb database from user john_doe.
REVOKE ALL PRIVILEGES ON imdb.* FROM 'root'@'localhost';

-- Q17: Insert a record into the genre table and commit the transaction.
START TRANSACTION;
INSERT INTO genre (movie_id, genre) VALUES ('tt1234567', 'Drama');
COMMIT;

-- Q18: Update a record in the movie table and commit the transaction.
START TRANSACTION;
UPDATE movie 
SET 
    duration = 140
WHERE
    id = 'tt1234567';
COMMIT;

-- Q19: Insert a record into the director_mapping table but rollback the transaction.
START TRANSACTION;
INSERT INTO director_mapping (movie_id, name_id) VALUES ('tt1234567', 'nm7654321');
ROLLBACK;

-- Q20: Update a record in the names table but rollback the transaction.
START TRANSACTION;
UPDATE names 
SET 
    height = 175
WHERE
    id = 'nm1234567';
ROLLBACK;

-- Q21: Retrieve the titles of movies along with their genres.
SELECT 
    movie.title, genre.genre
FROM
    movie
        INNER JOIN
    genre ON movie.id = genre.movie_id
LIMIT 12;

-- Q22: Retrieve director names for each movie.
SELECT 
    movie.title, names.name AS director_name
FROM
    movie
        INNER JOIN
    director_mapping ON movie.id = director_mapping.movie_id
        INNER JOIN
    names ON director_mapping.name_id = names.id
LIMIT 12;

-- Q23: Retrieve all movies and their genres, even if no genre is assigned.
SELECT 
    movie.title, genre.genre
FROM
    movie
        LEFT JOIN
    genre ON movie.id = genre.movie_id
LIMIT 12;

-- Q24: Retrieve all movies and their directors, even if no director is assigned.
SELECT 
    movie.title, names.name AS director_name
FROM
    movie
        LEFT JOIN
    director_mapping ON movie.id = director_mapping.movie_id
        LEFT JOIN
    names ON director_mapping.name_id = names.id
LIMIT 12;

-- Q25: Create a view to list all movies with their directors.
CREATE VIEW MovieDirectorView AS
    SELECT 
        movie.title AS MovieTitle, names.name AS DirectorName
    FROM
        movie
            INNER JOIN
        director_mapping ON movie.id = director_mapping.movie_id
            INNER JOIN
        names ON director_mapping.name_id = names.id;

-- Q26: Create a view to list movies along with their genres.
CREATE VIEW MovieGenreView AS
    SELECT 
        movie.title AS MovieTitle, genre.genre AS Genre
    FROM
        movie
            INNER JOIN
        genre ON movie.id = genre.movie_id;

-- Q27: Drop the view MovieDirectorView.
DROP VIEW MovieDirectorView;

-- Q28: Drop the view MovieGenreView.
DROP VIEW MovieGenreView;

SELECT * FROM MovieGenreView;

-- Q29: Create a procedure to insert a new movie.
DELIMITER //
CREATE PROCEDURE AddMovie(
    IN movieID VARCHAR(10),
    IN movieTitle VARCHAR(255),
    IN movieYear INT
)
BEGIN
    INSERT INTO movie (id, title, year)
    VALUES (movieID, movieTitle, movieYear);
END //
DELIMITER ;

-- Q30: Create a procedure to retrieve movies by genre.
DELIMITER //
CREATE PROCEDURE GetMoviesByGenre(
    IN genreName VARCHAR(50)
)
BEGIN
    SELECT movie.title
    FROM movie
    INNER JOIN genre ON movie.id = genre.movie_id
    WHERE genre.genre = genreName;
END //
DELIMITER ;

-- Q31: Create a function to calculate the average rating of a movie.
DELIMITER //
CREATE FUNCTION GetAverageRating(movieID VARCHAR(10))
RETURNS DECIMAL(3, 2)
DETERMINISTIC
BEGIN
    DECLARE avgRating DECIMAL(3, 2);
    SELECT AVG(rating) INTO avgRating FROM ratings WHERE movie_id = movieID;
    RETURN avgRating;
END //
DELIMITER ;

-- Q32: Create a function to calculate the total votes for a movie.
DELIMITER //
CREATE FUNCTION GetTotalVotes(movieID VARCHAR(10))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE totalVotes INT;
SELECT 
    SUM(total_votes)
INTO totalVotes FROM
    persons
WHERE
    movie_id = movieID;
    RETURN totalVotes;
END //
DELIMITER ;
