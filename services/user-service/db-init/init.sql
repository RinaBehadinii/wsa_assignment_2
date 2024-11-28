CREATE DATABASE IF NOT EXISTS user_db;

USE user_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

INSERT INTO users (name, email) VALUES
('John Doe', 'johndoe@example.com'),
('Jane Doe', 'janedoe@example.com');
