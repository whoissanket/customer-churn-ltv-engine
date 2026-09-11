from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib


# -------------------------------------------------
# CREATE FASTAPI APP
# -------------------------------------------------

app = FastAPI(
    title="Customer Churn & LTV Prediction API",
    description="API for customer churn prediction, LTV prediction and retention priority.",
    version="1.0.0"
)


# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------

churn_model = joblib.load("models/churn_model.joblib")
ltv_model = joblib.load("models/ltv_model.joblib")


# -------------------------------------------------
# LOAD TRAINING DATA
# Used for MonthlyCharges median and LTV thresholds
# -------------------------------------------------

training_data = pd.read_csv(
    "data/processed/final_features.csv"
)

monthly_charge_median = training_data["MonthlyCharges"].median()


# Load LTV prediction results to calculate thresholds
ltv_results = pd.read_csv(
    "reports/model_results/customer_ltv_predictions.csv"
)

# Find the predicted LTV column
if "PredictedLTV" in ltv_results.columns:
    ltv_values = ltv_results["PredictedLTV"]
elif "predicted_ltv" in ltv_results.columns:
    ltv_values = ltv_results["predicted_ltv"]
else:
    raise ValueError("Predicted LTV column not found.")


low_ltv_threshold = ltv_values.quantile(0.33)
high_ltv_threshold = ltv_values.quantile(0.67)


# -------------------------------------------------
# CUSTOMER INPUT MODEL
# -------------------------------------------------

class CustomerData(BaseModel):

    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# -------------------------------------------------
# PREPARE CUSTOMER FEATURES
# -------------------------------------------------

def prepare_features(customer: CustomerData):

    data = {
        "gender": customer.gender,
        "SeniorCitizen": customer.SeniorCitizen,
        "Partner": customer.Partner,
        "Dependents": customer.Dependents,
        "tenure": customer.tenure,
        "PhoneService": customer.PhoneService,
        "MultipleLines": customer.MultipleLines,
        "InternetService": customer.InternetService,
        "OnlineSecurity": customer.OnlineSecurity,
        "OnlineBackup": customer.OnlineBackup,
        "DeviceProtection": customer.DeviceProtection,
        "TechSupport": customer.TechSupport,
        "StreamingTV": customer.StreamingTV,
        "StreamingMovies": customer.StreamingMovies,
        "Contract": customer.Contract,
        "PaperlessBilling": customer.PaperlessBilling,
        "PaymentMethod": customer.PaymentMethod,
        "MonthlyCharges": customer.MonthlyCharges,
        "TotalCharges": customer.TotalCharges
    }

    df = pd.DataFrame([data])

    # Feature engineering
    df["TenureGroup"] = pd.cut(
        df["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=[
            "0-1 Year",
            "1-2 Years",
            "2-4 Years",
            "4+ Years"
        ]
    )

    df["AverageMonthlyRevenue"] = (
        df["TotalCharges"] /
        df["tenure"].replace(0, 1)
    )

    df["MonthlyToTotalRatio"] = (
        df["MonthlyCharges"] /
        (df["TotalCharges"] + 1)
    )

    df["IsLongTermCustomer"] = (
        df["tenure"] >= 24
    ).astype(int)

    df["HighMonthlyCharge"] = (
        df["MonthlyCharges"] >
        monthly_charge_median
    ).astype(int)

    return df


# -------------------------------------------------
# LTV SEGMENT
# -------------------------------------------------

def get_ltv_segment(ltv):

    if ltv >= high_ltv_threshold:
        return "High LTV"

    elif ltv >= low_ltv_threshold:
        return "Medium LTV"

    else:
        return "Low LTV"


# -------------------------------------------------
# CUSTOMER PRIORITY
# -------------------------------------------------

def get_priority(churn_probability, predicted_ltv):

    if (
        churn_probability >= 0.50
        and predicted_ltv >= high_ltv_threshold
    ):
        return "Critical - High Risk High Value"

    elif churn_probability >= 0.50:
        return "High Risk"

    elif predicted_ltv >= high_ltv_threshold:
        return "High Value"

    else:
        return "Low Priority"


# -------------------------------------------------
# HOME ENDPOINT
# -------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Customer Churn & LTV Prediction API",
        "status": "running"
    }


# -------------------------------------------------
# CHURN PREDICTION
# -------------------------------------------------

@app.post("/predict/churn")
def predict_churn(customer: CustomerData):

    df = prepare_features(customer)

    probability = churn_model.predict_proba(df)[0][1]

    prediction = int(
        churn_model.predict(df)[0]
    )

    return {
        "churn_probability": round(float(probability), 4),
        "predicted_churn": prediction,
        "churn_status": (
            "Likely to Churn"
            if prediction == 1
            else "Likely to Stay"
        )
    }


# -------------------------------------------------
# LTV PREDICTION
# -------------------------------------------------

@app.post("/predict/ltv")
def predict_ltv(customer: CustomerData):

    df = prepare_features(customer)

    # LTV model was trained without these columns
    ltv_input = df.drop(
        columns=["AverageMonthlyRevenue"]
    )

    predicted_ltv = ltv_model.predict(
        ltv_input
    )[0]

    segment = get_ltv_segment(
        predicted_ltv
    )

    return {
        "predicted_ltv": round(
            float(predicted_ltv), 2
        ),
        "ltv_segment": segment
    }


# -------------------------------------------------
# COMPLETE CUSTOMER PREDICTION
# -------------------------------------------------

@app.post("/predict/priority")
def predict_priority(customer: CustomerData):

    df = prepare_features(customer)

    # Churn prediction
    churn_probability = churn_model.predict_proba(
        df
    )[0][1]

    churn_prediction = int(
        churn_model.predict(df)[0]
    )

    # LTV prediction
    ltv_input = df.drop(
        columns=["AverageMonthlyRevenue"]
    )

    predicted_ltv = ltv_model.predict(
        ltv_input
    )[0]

    # Segment and priority
    ltv_segment = get_ltv_segment(
        predicted_ltv
    )

    priority = get_priority(
        churn_probability,
        predicted_ltv
    )

    return {
        "churn_probability": round(
            float(churn_probability), 4
        ),
        "predicted_churn": churn_prediction,
        "predicted_ltv": round(
            float(predicted_ltv), 2
        ),
        "ltv_segment": ltv_segment,
        "priority": priority
    }