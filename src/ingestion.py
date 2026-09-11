import pandas as pd

# Path of the raw dataset
DATA_PATH = "data/raw/telco_customer_churn.csv"


def load_data():
    # Load CSV file
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    return df


if __name__ == "__main__":
    df = load_data()

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())