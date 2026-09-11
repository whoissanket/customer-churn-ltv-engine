import pandas as pd
import joblib

# File paths
DATA_PATH = "data/processed/final_features.csv"
CHURN_MODEL_PATH = "models/churn_model.joblib"
LTV_MODEL_PATH = "models/ltv_model.joblib"
OUTPUT_PATH = "reports/model_results/customer_priority.csv"

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# --------------------------------------------------
# 2. Load trained models
# --------------------------------------------------

churn_model = joblib.load(CHURN_MODEL_PATH)
ltv_model = joblib.load(LTV_MODEL_PATH)

print("Churn model loaded successfully!")
print("LTV model loaded successfully!")

# --------------------------------------------------
# 3. Prepare features for prediction
# --------------------------------------------------

X = df.drop(columns=["Churn"])

# Churn model prediction
churn_probability = churn_model.predict_proba(X)[:, 1]

# LTV model does not use Churn or AverageMonthlyRevenue
X_ltv = X.drop(columns=["AverageMonthlyRevenue"])

# LTV prediction
predicted_ltv = ltv_model.predict(X_ltv)

# --------------------------------------------------
# 4. Add predictions
# --------------------------------------------------

df["ChurnProbability"] = churn_probability
df["PredictedLTV"] = predicted_ltv

# --------------------------------------------------
# 5. Calculate LTV threshold
# --------------------------------------------------

high_ltv_threshold = df["PredictedLTV"].quantile(0.67)

print("\nHigh LTV threshold:", round(high_ltv_threshold, 2))

# --------------------------------------------------
# 6. Create customer priority
# --------------------------------------------------

def assign_priority(row):

    if row["ChurnProbability"] >= 0.50 and row["PredictedLTV"] >= high_ltv_threshold:
        return "Critical - High Risk High Value"

    elif row["ChurnProbability"] >= 0.50:
        return "High Risk"

    elif row["PredictedLTV"] >= high_ltv_threshold:
        return "High Value"

    else:
        return "Low Priority"


df["Priority"] = df.apply(assign_priority, axis=1)

# --------------------------------------------------
# 7. Save priority results
# --------------------------------------------------

output_columns = [
    "gender",
    "tenure",
    "Contract",
    "InternetService",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
    "ChurnProbability",
    "PredictedLTV",
    "Priority"
]

df[output_columns].to_csv(
    OUTPUT_PATH,
    index=False
)

# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER PRIORITY ENGINE")
print("=" * 60)

print("\nPriority distribution:")
print(df["Priority"].value_counts())

print("\nTop 10 high-priority customers:")

top_customers = df.sort_values(
    by=["ChurnProbability", "PredictedLTV"],
    ascending=[False, False]
)

print(
    top_customers[
        [
            "tenure",
            "Contract",
            "MonthlyCharges",
            "ChurnProbability",
            "PredictedLTV",
            "Priority"
        ]
    ].head(10)
)

print("\nPriority engine completed successfully!")

print("\nResults saved to:")
print(OUTPUT_PATH)