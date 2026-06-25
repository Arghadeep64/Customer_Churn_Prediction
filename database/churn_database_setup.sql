CREATE DATABASE IF NOT EXISTS churn_db;

USE churn_db;



CREATE TABLE IF NOT EXISTS customers(

    customer_id INT PRIMARY KEY AUTO_INCREMENT,

    gender VARCHAR(10),

    senior_citizen BOOLEAN,

    partner VARCHAR(5),

    dependents VARCHAR(5),

    tenure INT,

    phone_service VARCHAR(5),

    internet_service VARCHAR(20),

    contract_type VARCHAR(20),

    payment_method VARCHAR(50),

    monthly_charges DECIMAL(10,2),

    total_charges DECIMAL(10,2),

    churn VARCHAR(5)

);



CREATE TABLE IF NOT EXISTS users(

    id INT PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(50) UNIQUE NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL

);



CREATE TABLE IF NOT EXISTS prediction_history(

    id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT,

    username VARCHAR(50),

    gender VARCHAR(10),

    senior_citizen VARCHAR(5),

    partner VARCHAR(5),

    dependents VARCHAR(5),

    tenure INT,

    phone_service VARCHAR(5),

    multiple_lines VARCHAR(5),

    internet_service VARCHAR(20),

    online_security VARCHAR(5),

    online_backup VARCHAR(5),

    device_protection VARCHAR(5),

    tech_support VARCHAR(5),

    streaming_tv VARCHAR(5),

    streaming_movies VARCHAR(5),

    contract VARCHAR(20),

    paperless_billing VARCHAR(5),

    payment_method VARCHAR(50),

    monthly_charges FLOAT,

    prediction VARCHAR(30),

    confidence FLOAT,

    prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)

    REFERENCES users(id)

);



SHOW TABLES;

DESC users;

DESC prediction_history;

SELECT * FROM users;

SELECT * FROM prediction_history;