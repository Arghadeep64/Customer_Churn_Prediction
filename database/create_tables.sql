-- Create database tables for Customer Churn Prediction

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    account_length INT,
    service_area VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customer features table
CREATE TABLE IF NOT EXISTS customer_features (
    feature_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(10, 2),
    internet_service VARCHAR(50),
    online_security VARCHAR(10),
    online_backup VARCHAR(10),
    device_protection VARCHAR(10),
    tech_support VARCHAR(10),
    streaming_tv VARCHAR(10),
    streaming_movies VARCHAR(10),
    contract VARCHAR(50),
    paperless_billing VARCHAR(10),
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    prediction INT,
    probability DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Model performance table
CREATE TABLE IF NOT EXISTS model_performance (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    model_name VARCHAR(100),
    accuracy DECIMAL(5, 4),
    precision DECIMAL(5, 4),
    recall DECIMAL(5, 4),
    f1_score DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_customer_email ON customers(email);
CREATE INDEX idx_prediction_customer ON predictions(customer_id);
CREATE INDEX idx_feature_customer ON customer_features(customer_id);
