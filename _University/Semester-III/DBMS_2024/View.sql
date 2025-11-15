USE imdb;

SELECT * FROM movie;

SELECT * FROM genre;

CREATE OR REPLACE VIEW movieRecordsByCountry AS
    SELECT 
        *
    FROM
        movie
    WHERE
        country IN ('Germany' , 'UK', 'USA')
    ORDER BY country;
        
SELECT * FROM movieRecords;

SELECT m.id, m.title, g.genre FROM movie m
INNER JOIN genre g ON m.id = g.movie_id
ORDER BY genre, id;