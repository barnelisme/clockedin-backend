CREATE DATABASE clockedin;
USE clockedin;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    picture BLOB
);

CREATE TABLE staff_users (
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100) NOT NULL,
    staff_number VARCHAR(20) UNIQUE NOT NULL,
    contact_number VARCHAR(20),
    department VARCHAR(50),
    UNIQUE KEY (staff_number)
);
