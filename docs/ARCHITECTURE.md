# System Architecture

## Overview

The Customer Churn & LTV Engine follows a modular analytics architecture
combining data processing, machine learning, database analytics, API
services and an interactive dashboard.

## Architecture Flow

```text
                 Telco Customer Dataset
                          |
                          v
                  Data Ingestion
                          |
                          v
                Data Preprocessing
                          |
                          v
                 Feature Engineering
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Churn Prediction          LTV Engine
              |                       |
              v                       v
         SHAP Analysis        LTV Segmentation
              |                       |
              +-----------+-----------+
                          |
                          v
                Customer Priority
                     Engine
                          |
              +-----------+-----------+
              |                       |
              v                       v
         PostgreSQL                ML Models
              |                       |
              v                       v
        SQL Analytics             FastAPI
                                      |
                                      v
                                Streamlit
                                 Dashboard
                                 