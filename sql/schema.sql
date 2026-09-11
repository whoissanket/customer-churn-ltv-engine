CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    gender VARCHAR(20),
    senior_citizen INTEGER,
    partner VARCHAR(10),
    dependents VARCHAR(10),
    tenure INTEGER,
    phone_service VARCHAR(20),
    multiple_lines VARCHAR(30),
    internet_service VARCHAR(30),
    online_security VARCHAR(30),
    online_backup VARCHAR(30),
    device_protection VARCHAR(30),
    tech_support VARCHAR(30),
    streaming_tv VARCHAR(30),
    streaming_movies VARCHAR(30),
    contract VARCHAR(50),
    paperless_billing VARCHAR(10),
    payment_method VARCHAR(50),
    monthly_charges DECIMAL(10,2),
    total_charges DECIMAL(10,2),
    churn INTEGER,
    tenure_group VARCHAR(30),
    average_monthly_revenue DECIMAL(10,2),
    monthly_to_total_ratio DECIMAL(10,4),
    is_long_term_customer INTEGER,
    high_monthly_charge INTEGER
);

CREATE TABLE IF NOT EXISTS churn_predictions (
    prediction_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    churn_probability DECIMAL(10,6),
    predicted_churn INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ltv_predictions (
    prediction_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    predicted_ltv DECIMAL(12,2),
    ltv_segment VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_priority (
    priority_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    churn_probability DECIMAL(10,6),
    predicted_ltv DECIMAL(12,2),
    priority VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);