 -- =========================================
-- 1️. CREATE DATABASE
-- =========================================

-- Create new database
CREATE DATABASE movie_recommendation;

-- Select the database to work on
USE movie_recommendation;


-- =========================================
-- 2️. CREATE TABLES
-- =========================================


-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255)
);

-- Movies table
CREATE TABLE movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(255),
    genres VARCHAR(255)
);

-- Ratings table
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    rating FLOAT,
    timestamp BIGINT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- =========================================
-- ️3. VIEW DATA
-- =========================================

SELECT * FROM movies;
SELECT * FROM ratings;
SELECT * FROM ratings ORDER BY rating_id DESC LIMIT 10;