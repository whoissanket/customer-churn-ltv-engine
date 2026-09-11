import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = "data/processed/final_features.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# 2. CREATE LTV TARGET
# ============================================================

# Estimate average monthly revenue
df["AverageMonthlyRevenue"] = (
    df["TotalCharges"] /
    df["tenure"].replace(0, 1)
)

# Estimate expected remaining months
# based on current tenure and customer lifecycle
expected_lifetime_months = np.maximum(
    df["tenure"],
    12
)

# Estimated customer lifetime value
df["EstimatedLTV"] = (
    df["AverageMonthlyRevenue"] *
    expected_lifetime_months
)


print("\nLTV statistics:")
print(df["EstimatedLTV"].describe())


# ============================================================
# 3. PREPARE FEATURES
# ============================================================

# Remove target and derived LTV columns
X = df.drop(
    columns=[
        "Churn",
        "EstimatedLTV",
        "AverageMonthlyRevenue"
    ]
)

y = df["EstimatedLTV"]


# ============================================================
# 4. IDENTIFY COLUMN TYPES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numerical_columns)


# ============================================================
# 5. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_columns
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_columns
        )
    ]
)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 7. LTV REGRESSION MODEL
# ============================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 8. TRAIN MODEL
# ============================================================

print("\nTraining LTV model...")

pipeline.fit(
    X_train,
    y_train
)


# ============================================================
# 9. PREDICTION
# ============================================================

y_pred = pipeline.predict(X_test)


# ============================================================
# 10. EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)

r2 = r2_score(
    y_test,
    y_pred
)


print("\n" + "=" * 60)
print("LTV MODEL RESULTS")
print("=" * 60)

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R²  :", round(r2, 4))


# ============================================================
# 11. SAVE MODEL
# ============================================================

MODEL_PATH = "models/ltv_model.joblib"

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nLTV model saved successfully!")
print("Model path:", MODEL_PATH)


# ============================================================
# 12. CREATE LTV PREDICTIONS
# ============================================================

df["PredictedLTV"] = pipeline.predict(X)


# ============================================================
# 13. CREATE LTV SEGMENTS
# ============================================================

df["LTVSegment"] = pd.qcut(
    df["PredictedLTV"],
    q=3,
    labels=[
        "Low LTV",
        "Medium LTV",
        "High LTV"
    ],
    duplicates="drop"
)


# ============================================================
# 14. SAVE LTV RESULTS
# ============================================================

OUTPUT_PATH = "reports/model_results/customer_ltv_predictions.csv"

df[
    [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
        "PredictedLTV",
        "LTVSegment"
    ]
].to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nLTV predictions saved to:")
print(OUTPUT_PATH)

print("\nLTV segment distribution:")
print(df["LTVSegment"].value_counts())

print("\nLTV model completed successfully!")