# Customer Churn & LTV Engine — API Documentation

## 1. Overview

The Customer Churn & LTV Engine provides a REST API built using FastAPI.

The API exposes machine learning predictions for:

- Customer churn probability
- Estimated customer lifetime value (LTV)
- LTV segmentation
- Customer retention priority

The API is used by the Streamlit dashboard to provide interactive customer
predictions.

---

# 2. Technology

- Python
- FastAPI
- Pydantic
- Scikit-learn
- XGBoost
- Joblib
- Pandas
- Uvicorn

---

# 3. Running the API

From the project root directory, activate the virtual environment and run:

```bash
uvicorn api.main:app --reload
