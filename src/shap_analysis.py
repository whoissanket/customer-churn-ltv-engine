import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = "data/processed/final_features.csv"
MODEL_PATH = "models/churn_model.joblib"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# ============================================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================================

X = df.drop(columns=["Churn"])
y = df["Churn"]


# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

model = joblib.load(MODEL_PATH)

print("Trained model loaded successfully!")


# ============================================================
# 4. GET PREPROCESSOR AND MODEL
# ============================================================

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["model"]


# ============================================================
# 5. TRANSFORM DATA
# ============================================================

X_transformed = preprocessor.transform(X)

print("Data transformed successfully!")


# ============================================================
# 6. GET FEATURE NAMES
# ============================================================

feature_names = preprocessor.get_feature_names_out()


# ============================================================
# 7. CREATE SHAP EXPLAINER
# ============================================================

explainer = shap.LinearExplainer(
    classifier,
    X_transformed
)

shap_values = explainer(X_transformed)


# ============================================================
# 8. GLOBAL FEATURE IMPORTANCE
# ============================================================

print("\nCreating SHAP summary plot...")

plt.figure()

shap.summary_plot(
    shap_values,
    X_transformed,
    feature_names=feature_names,
    show=False
)

plt.title("SHAP Feature Importance - Churn Model")

plt.tight_layout()

plt.savefig(
    "reports/figures/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "SHAP summary saved to: "
    "reports/figures/shap_summary.png"
)


# ============================================================
# 9. BAR IMPORTANCE PLOT
# ============================================================

plt.figure()

shap.summary_plot(
    shap_values,
    X_transformed,
    feature_names=feature_names,
    plot_type="bar",
    show=False
)

plt.title("SHAP Global Feature Importance")

plt.tight_layout()

plt.savefig(
    "reports/figures/shap_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "SHAP feature importance saved to: "
    "reports/figures/shap_feature_importance.png"
)


# ============================================================
# 10. TOP FEATURES
# ============================================================

importance = pd.DataFrame({
    "Feature": feature_names,
    "MeanAbsoluteSHAP": abs(
        shap_values.values
    ).mean(axis=0)
})

importance = importance.sort_values(
    "MeanAbsoluteSHAP",
    ascending=False
)

print("\nTop 15 Churn Drivers:")

print(
    importance.head(15).to_string(
        index=False
    )
)


# ============================================================
# 11. SAVE FEATURE IMPORTANCE
# ============================================================

importance.to_csv(
    "reports/model_results/shap_feature_importance.csv",
    index=False
)

print(
    "\nSHAP analysis completed successfully!"
)