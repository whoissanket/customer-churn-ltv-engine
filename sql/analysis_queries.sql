-- ============================================================
-- CUSTOMER CHURN & LTV ENGINE
-- SQL ANALYTICS QUERIES
-- ============================================================


-- ============================================================
-- 1. Overall Customer Statistics
-- ============================================================

SELECT
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    COUNT(*) - SUM(churn) AS retained_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers;


-- ============================================================
-- 2. Churn by Contract Type
-- ============================================================

SELECT
    contract,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;


-- ============================================================
-- 3. Churn by Internet Service
-- ============================================================

SELECT
    internet_service,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY internet_service
ORDER BY churn_rate DESC;


-- ============================================================
-- 4. Churn by Tenure Group
-- ============================================================

SELECT
    tenure_group,
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    ROUND(
        100.0 * SUM(churn) / COUNT(*),
        2
    ) AS churn_rate
FROM customers
GROUP BY tenure_group
ORDER BY churn_rate DESC;


-- ============================================================
-- 5. Average Monthly Charges by Churn Status
-- ============================================================

SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS average_monthly_charges,
    ROUND(AVG(total_charges), 2) AS average_total_charges
FROM customers
GROUP BY churn
ORDER BY churn DESC;


-- ============================================================
-- 6. Highest Churn Risk Customers
-- ============================================================

SELECT
    cp.customer_id,
    c.tenure,
    c.contract,
    c.internet_service,
    c.monthly_charges,
    cp.churn_probability
FROM churn_predictions cp
JOIN customers c
    ON cp.customer_id = c.customer_id
ORDER BY cp.churn_probability DESC
LIMIT 20;


-- ============================================================
-- 7. Highest LTV Customers
-- ============================================================

SELECT
    lp.customer_id,
    c.tenure,
    c.contract,
    c.internet_service,
    c.monthly_charges,
    lp.predicted_ltv,
    lp.ltv_segment
FROM ltv_predictions lp
JOIN customers c
    ON lp.customer_id = c.customer_id
ORDER BY lp.predicted_ltv DESC
LIMIT 20;


-- ============================================================
-- 8. Critical Customers
-- High Churn Risk + High LTV
-- ============================================================

SELECT
    cp.customer_id,
    cp.churn_probability,
    lp.predicted_ltv,
    p.priority
FROM churn_predictions cp
JOIN ltv_predictions lp
    ON cp.customer_id = lp.customer_id
JOIN customer_priority p
    ON cp.customer_id = p.customer_id
WHERE p.priority = 'Critical - High Risk High Value'
ORDER BY
    cp.churn_probability DESC,
    lp.predicted_ltv DESC;


-- ============================================================
-- 9. Priority Segment Summary
-- ============================================================

SELECT
    priority,
    COUNT(*) AS customer_count,
    ROUND(AVG(churn_probability), 4)
        AS average_churn_probability,
    ROUND(AVG(predicted_ltv), 2)
        AS average_predicted_ltv
FROM customer_priority
GROUP BY priority
ORDER BY average_churn_probability DESC;


-- ============================================================
-- 10. High Risk Customers by Contract
-- ============================================================

SELECT
    c.contract,
    COUNT(*) AS high_risk_customers,
    ROUND(
        AVG(cp.churn_probability),
        4
    ) AS average_churn_probability
FROM churn_predictions cp
JOIN customers c
    ON cp.customer_id = c.customer_id
WHERE cp.churn_probability >= 0.50
GROUP BY c.contract
ORDER BY high_risk_customers DESC;


-- ============================================================
-- 11. High Value Customers by Internet Service
-- ============================================================

SELECT
    c.internet_service,
    COUNT(*) AS high_value_customers,
    ROUND(
        AVG(lp.predicted_ltv),
        2
    ) AS average_ltv
FROM ltv_predictions lp
JOIN customers c
    ON lp.customer_id = c.customer_id
WHERE lp.predicted_ltv >= (
    SELECT
        PERCENTILE_CONT(0.67)
        WITHIN GROUP (
            ORDER BY predicted_ltv
        )
    FROM ltv_predictions
)
GROUP BY c.internet_service
ORDER BY average_ltv DESC;


-- ============================================================
-- 12. Retention Target List
-- High churn probability customers
-- ============================================================

SELECT
    p.customer_id,
    p.churn_probability,
    p.predicted_ltv,
    p.priority,
    c.contract,
    c.tenure,
    c.monthly_charges
FROM customer_priority p
JOIN customers c
    ON p.customer_id = c.customer_id
WHERE p.churn_probability >= 0.50
ORDER BY
    p.predicted_ltv DESC,
    p.churn_probability DESC
LIMIT 100;