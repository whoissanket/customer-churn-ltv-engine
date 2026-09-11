import pandas as pd

INPUT_PATH = "data/processed/cleaned_telco_customer_churn.csv"
OUTPUT_PATH = "data/processed/final_features.csv"


def create_features(df):

    df = df.copy()

    # 1. Customer tenure group
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

    # 2. Average monthly revenue
    df["AverageMonthlyRevenue"] = (
        df["TotalCharges"] /
        df["tenure"].replace(0, 1)
    )

    # 3. Monthly charges compared with total charges
    df["MonthlyToTotalRatio"] = (
        df["MonthlyCharges"] /
        (df["TotalCharges"] + 1)
    )

    # 4. Long-term customer flag
    df["IsLongTermCustomer"] = (
        df["tenure"] >= 24
    ).astype(int)

    # 5. High monthly charge flag
    median_monthly_charge = df["MonthlyCharges"].median()

    df["HighMonthlyCharge"] = (
        df["MonthlyCharges"] > median_monthly_charge
    ).astype(int)

    return df


if __name__ == "__main__":

    # Load cleaned dataset
    df = pd.read_csv(INPUT_PATH)

    print("Before feature engineering:")
    print(df.shape)

    # Create new features
    df = create_features(df)

    print("\nAfter feature engineering:")
    print(df.shape)

    print("\nNew features created:")
    print("1. TenureGroup")
    print("2. AverageMonthlyRevenue")
    print("3. MonthlyToTotalRatio")
    print("4. IsLongTermCustomer")
    print("5. HighMonthlyCharge")

    # Save final dataset
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nFeature engineering completed successfully!")
    print("Saved to:", OUTPUT_PATH)