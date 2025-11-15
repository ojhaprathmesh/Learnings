CREATE DATABASE MovieDatabase;
USE MovieDatabase;

CREATE TABLE Movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    genre VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 1) CHECK (rating >= 0 AND rating <= 10) NOT NULL,
    director VARCHAR(255) NOT NULL
);

CREATE TABLE Actors (
    actor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')) NOT NULL,
    movie_id INT,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

INSERT INTO Movies (title, release_year, genre, rating, director)
VALUES
('Inception', 2010, 'Sci-Fi', 8.8, 'Christopher Nolan'),
('The Dark Knight', 2008, 'Action', 9.0, 'Christopher Nolan'),
('Interstellar', 2014, 'Sci-Fi', 8.6, 'Christopher Nolan'),
('The Godfather', 1972, 'Crime', 9.2, 'Francis Ford Coppola'),
('Pulp Fiction', 1994, 'Crime', 8.9, 'Quentin Tarantino'),
('Fight Club', 1999, 'Drama', 8.8, 'David Fincher'),
('The Matrix', 1999, 'Sci-Fi', 8.7, 'The Wachowskis'),
('Forrest Gump', 1994, 'Drama', 8.8, 'Robert Zemeckis'),
('The Shawshank Redemption', 1994, 'Drama', 9.3, 'Frank Darabont'),
('The Lord of the Rings: The Return of the King', 2003, 'Fantasy', 8.9, 'Peter Jackson');

INSERT INTO Actors (name, birth_year, gender, movie_id)
VALUES
('Leonardo DiCaprio', 1974, 'M', 1),
('Joseph Gordon-Levitt', 1981, 'M', 1),
('Christian Bale', 1974, 'M', 2),
('Heath Ledger', 1979, 'M', 2),
('Marlon Brando', 1924, 'M', 4),
('Al Pacino', 1940, 'M', 4),
('John Travolta', 1954, 'M', 5),
('Uma Thurman', 1970, 'F', 5),
('Edward Norton', 1969, 'M', 6),
('Brad Pitt', 1963, 'M', 6);

SELECT * FROM Movies;

SELECT title, release_year FROM Movies;

SELECT * FROM Movies
WHERE director = 'Christopher Nolan';

SELECT * FROM Actors
WHERE birth_year < 1970;

SELECT * FROM Movies
WHERE rating > 8.5;

SELECT * FROM Movies
WHERE release_year > 2000;

SELECT * FROM Actors
WHERE gender = 'M';

SELECT * FROM Movies
WHERE genre = 'Sci-Fi';

SELECT * FROM Actors
WHERE birth_year < 1980 AND birth_year < 1980;

SELECT * FROM Movies
WHERE genre = 'Sci-Fi' OR genre = 'Drama';

SELECT * FROM Actors
WHERE gender = 'F' AND birth_year > 1970;

SELECT * FROM Movies
WHERE rating > 8.5 AND release_year < 2010;

SELECT * FROM Actors
WHERE gender = 'M' OR birth_year > 1980;

SELECT * FROM Movies
WHERE NOT director = 'Christopher Nolan';

SELECT * FROM Actors
WHERE NOT gender = 'M';

SELECT * FROM Movies
WHERE NOT genre = 'Drama';

SELECT * FROM Movies
ORDER BY rating DESC
LIMIT 5;

SELECT * FROM Actors
ORDER BY birth_year DESC;

SELECT * FROM Movies
ORDER BY release_year DESC
LIMIT 3;

SELECT genre FROM Movies
GROUP BY genre
HAVING AVG(rating) > 8.5;

SELECT director, COUNT(title) AS movie_count FROM Movies
GROUP BY director
HAVING movie_count > 1;
