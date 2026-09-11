# Customer Churn & Lifetime Value Engine

A production-oriented customer analytics and machine learning platform for
predicting customer churn, estimating customer lifetime value (LTV), and
prioritizing customers for retention actions.

The project combines machine learning, explainable AI, PostgreSQL, SQL
analytics, FastAPI and Streamlit into an end-to-end customer intelligence
system.

---

## Project Overview

Customer churn is a major business problem because acquiring a new customer
can be significantly more expensive than retaining an existing customer.

This project analyzes customer behavior and provides a system that can:

- Identify customers at risk of churn
- Estimate customer lifetime value
- Explain important churn drivers
- Identify high-value customers
- Prioritize customers for retention campaigns
- Provide real-time predictions through an API
- Display business insights through an interactive dashboard

The project was structured as a 12-week / 3-month end-to-end development
project covering data engineering, machine learning, database integration,
API development, dashboard development and final testing.

---

# Key Results

| Metric | Result |
|---|---:|
| Customers analyzed | 7,032 |
| Overall churn rate | 26.58% |
| High-risk customers | 1,375 |
| Critical customers | 140 |
| High-value customers | 2,181 |
| Best churn model | Logistic Regression |
| Best F1-score | 59.25% |
| Average estimated LTV | $2,406.34 |

---

# Problem Statement

The objective is to build a customer analytics platform that can transform
historical customer data into actionable retention insights.

The system combines churn prediction and customer value estimation so that
business teams can focus retention efforts on customers who represent a
higher business priority.

---

# Project Objectives

1. Analyze customer behavior and churn patterns.
2. Clean and preprocess customer data.
3. Engineer features useful for churn prediction.
4. Build and compare multiple churn prediction models.
5. Explain model predictions using SHAP.
6. Develop an estimated customer LTV engine.
7. Build a customer priority and retention engine.
8. Store analytics data in PostgreSQL.
9. Develop SQL-based business analytics.
10. Expose predictions through FastAPI.
11. Build an interactive Streamlit dashboard.
12. Test and document the complete system.

---

# Dataset

The project uses the Telco Customer Churn dataset.

The dataset contains approximately 7,000 customer records with information
about:

- Demographics
- Tenure
- Services
- Contract type
- Payment method
- Monthly charges
- Total charges
- Customer churn

After preprocessing, 7,032 usable customer records were retained.

The raw dataset is intentionally excluded from GitHub through `.gitignore`.

---

# Technology Stack

## Programming

- Python

## Data Processing

- Pandas
- NumPy

## Machine Learning

- Scikit-learn
- XGBoost
- Random Forest

## Explainable AI

- SHAP

## Database

- PostgreSQL
- SQLAlchemy
- psycopg2

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Dashboard

- Streamlit
- Plotly

## Development

- VS Code
- Git
- GitHub

---

# System Architecture

```text
                    TELCO CUSTOMER DATA
                            |
                            v
                    DATA INGESTION
                            |
                            v
                  DATA PREPROCESSING
                            |
                            v
                  FEATURE ENGINEERING
                            |
             +--------------+--------------+
             |                             |
             v                             v
      CHURN PREDICTION                LTV ENGINE
             |                             |
             v                             v
       SHAP ANALYSIS                LTV SEGMENTATION
             |                             |
             +--------------+--------------+
                            |
                            v
                  CUSTOMER PRIORITY
                       ENGINE
                            |
                 +----------+----------+
                 |                     |
                 v                     v
            PostgreSQL              ML Models
                 |                     |
                 v                     v
           SQL Analytics            FastAPI
                                       |
                                       v
                                  Streamlit
                                   Dashboard