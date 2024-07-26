-- create-tables.sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    user_name VARCHAR(64) NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL
);