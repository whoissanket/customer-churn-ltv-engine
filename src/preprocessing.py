import pandas as pd

# Path of raw dataset
DATA_PATH = "data/raw/telco_customer_churn.csv"

# Path for processed dataset
OUTPUT_PATH = "data/processed/cleaned_telco_customer_churn.csv"


def preprocess_data():

    # Load dataset
    df = pd.read_csv(DATA_PATH)

    print("Original dataset shape:", df.shape)

    # Convert TotalCharges from text to numeric
    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    # Check missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum())

    # Remove rows where TotalCharges is missing
    df = df.dropna(subset=["TotalCharges"])

    # Remove Customer ID because it is not useful for prediction
    df = df.drop(columns=["customerID"])

    # Convert Churn into numerical values
    df["Churn"] = df["Churn"].map({
        "Yes": 1,
        "No": 0
    })

    print("\nDataset shape after cleaning:", df.shape)

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    # Save cleaned dataset
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nCleaned dataset saved successfully!")
    print("File:", OUTPUT_PATH)

    return df


if __name__ == "__main__":
    df = preprocess_data()

    print("\nFirst 5 rows of cleaned dataset:")
    print(df.head())