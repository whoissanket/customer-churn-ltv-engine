import pandas as pd
from database import engine


FEATURES_PATH = "data/processed/final_features.csv"
PRIORITY_PATH = "reports/model_results/customer_priority.csv"


def load_customers():
    print("Loading customer data...")

    df = pd.read_csv(FEATURES_PATH)

    df = df.rename(columns={
        "SeniorCitizen": "senior_citizen",
        "Partner": "partner",
        "Dependents": "dependents",
        "PhoneService": "phone_service",
        "MultipleLines": "multiple_lines",
        "InternetService": "internet_service",
        "OnlineSecurity": "online_security",
        "OnlineBackup": "online_backup",
        "DeviceProtection": "device_protection",
        "TechSupport": "tech_support",
        "StreamingTV": "streaming_tv",
        "StreamingMovies": "streaming_movies",
        "Contract": "contract",
        "PaperlessBilling": "paperless_billing",
        "PaymentMethod": "payment_method",
        "MonthlyCharges": "monthly_charges",
        "TotalCharges": "total_charges",
        "Churn": "churn",
        "TenureGroup": "tenure_group",
        "AverageMonthlyRevenue": "average_monthly_revenue",
        "MonthlyToTotalRatio": "monthly_to_total_ratio",
        "IsLongTermCustomer": "is_long_term_customer",
        "HighMonthlyCharge": "high_monthly_charge"
    })

    df.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Customers loaded successfully!")
    print("Customers inserted:", len(df))


def load_predictions():
    print("\nLoading prediction data...")

    priority_df = pd.read_csv(PRIORITY_PATH)

    print("\nPriority file columns:")
    print(priority_df.columns.tolist())

    # Create customer IDs
    priority_df["customer_id"] = range(1, len(priority_df) + 1)

    # Rename prediction columns
    priority_df = priority_df.rename(columns={
        "ChurnProbability": "churn_probability",
        "PredictedLTV": "predicted_ltv",
        "Priority": "priority"
    })

    # -----------------------------
    # CHURN PREDICTIONS
    # -----------------------------

    churn_df = priority_df[
        ["customer_id", "churn_probability"]
    ].copy()

    churn_df["predicted_churn"] = (
        churn_df["churn_probability"] >= 0.5
    ).astype(int)

    churn_df.to_sql(
        "churn_predictions",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Churn predictions loaded successfully!")

    # -----------------------------
    # LTV PREDICTIONS
    # -----------------------------

    ltv_df = priority_df[
        ["customer_id", "predicted_ltv"]
    ].copy()

    low_threshold = ltv_df["predicted_ltv"].quantile(0.33)
    high_threshold = ltv_df["predicted_ltv"].quantile(0.67)

    def get_ltv_segment(value):
        if value >= high_threshold:
            return "High LTV"
        elif value >= low_threshold:
            return "Medium LTV"
        else:
            return "Low LTV"

    ltv_df["ltv_segment"] = ltv_df[
        "predicted_ltv"
    ].apply(get_ltv_segment)

    ltv_df.to_sql(
        "ltv_predictions",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("LTV predictions loaded successfully!")

    # -----------------------------
    # CUSTOMER PRIORITY
    # -----------------------------

    customer_priority_df = priority_df[
        [
            "customer_id",
            "churn_probability",
            "predicted_ltv",
            "priority"
        ]
    ].copy()

    customer_priority_df.to_sql(
        "customer_priority",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("Customer priority data loaded successfully!")


def main():
    print("=" * 60)
    print("LOADING DATA INTO POSTGRESQL")
    print("=" * 60)

    load_customers()
    load_predictions()

    print("\n" + "=" * 60)
    print("DATABASE LOADING COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()