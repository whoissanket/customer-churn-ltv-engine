import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.database import engine


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Churn & LTV Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Customer Churn & Lifetime Value Dashboard")
st.markdown(
    "Customer retention, churn risk, LTV and priority analysis"
)

st.divider()


# --------------------------------------------------
# DATABASE FUNCTIONS
# --------------------------------------------------

@st.cache_data
def load_customer_data():

    query = """
    SELECT *
    FROM customers
    """

    return pd.read_sql(query, engine)


@st.cache_data
def load_churn_predictions():

    query = """
    SELECT *
    FROM churn_predictions
    """

    return pd.read_sql(query, engine)


@st.cache_data
def load_ltv_predictions():

    query = """
    SELECT *
    FROM ltv_predictions
    """

    return pd.read_sql(query, engine)


@st.cache_data
def load_priority_data():

    query = """
    SELECT *
    FROM customer_priority
    """

    return pd.read_sql(query, engine)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    customers = load_customer_data()
    churn_predictions = load_churn_predictions()
    ltv_predictions = load_ltv_predictions()
    priority_data = load_priority_data()

except Exception as e:

    st.error("Unable to connect to PostgreSQL database.")

    st.code(str(e))

    st.stop()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_customers = len(customers)

churned_customers = customers["churn"].sum()

churn_rate = (
    churned_customers / total_customers
) * 100

high_risk_customers = len(
    priority_data[
        priority_data["priority"] == "High Risk"
    ]
)

critical_customers = len(
    priority_data[
        priority_data["priority"]
        == "Critical - High Risk High Value"
    ]
)

high_value_customers = len(
    priority_data[
        priority_data["priority"] == "High Value"
    ]
)

average_ltv = ltv_predictions["predicted_ltv"].mean()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📌 Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:

    st.metric(
        "Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col3:

    st.metric(
        "High Risk",
        f"{high_risk_customers:,}"
    )

with col4:

    st.metric(
        "Critical Customers",
        f"{critical_customers:,}"
    )

with col5:

    st.metric(
        "Average LTV",
        f"${average_ltv:,.2f}"
    )


st.divider()


# --------------------------------------------------
# CHURN ANALYSIS
# --------------------------------------------------

st.subheader("📈 Churn Analysis")

col1, col2 = st.columns(2)


# Churn by Contract

with col1:

    contract_data = customers.groupby(
        "contract"
    ).agg(
        total_customers=("customer_id", "count"),
        churned=("churn", "sum")
    ).reset_index()

    contract_data["churn_rate"] = (
        contract_data["churned"]
        / contract_data["total_customers"]
    ) * 100

    fig_contract = px.bar(
        contract_data,
        x="contract",
        y="churn_rate",
        title="Churn Rate by Contract Type",
        labels={
            "contract": "Contract",
            "churn_rate": "Churn Rate (%)"
        },
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_contract,
        use_container_width=True
    )


# Churn by Internet Service

with col2:

    internet_data = customers.groupby(
        "internet_service"
    ).agg(
        total_customers=("customer_id", "count"),
        churned=("churn", "sum")
    ).reset_index()

    internet_data["churn_rate"] = (
        internet_data["churned"]
        / internet_data["total_customers"]
    ) * 100

    fig_internet = px.bar(
        internet_data,
        x="internet_service",
        y="churn_rate",
        title="Churn Rate by Internet Service",
        labels={
            "internet_service": "Internet Service",
            "churn_rate": "Churn Rate (%)"
        },
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_internet,
        use_container_width=True
    )


# --------------------------------------------------
# TENURE ANALYSIS
# --------------------------------------------------

st.subheader("👥 Customer Tenure Analysis")

tenure_data = customers.groupby(
    "tenure_group"
).agg(
    total_customers=("customer_id", "count"),
    churned=("churn", "sum")
).reset_index()

tenure_data["churn_rate"] = (
    tenure_data["churned"]
    / tenure_data["total_customers"]
) * 100

fig_tenure = px.bar(
    tenure_data,
    x="tenure_group",
    y="churn_rate",
    title="Churn Rate by Customer Tenure",
    labels={
        "tenure_group": "Tenure Group",
        "churn_rate": "Churn Rate (%)"
    },
    text_auto=".2f"
)

st.plotly_chart(
    fig_tenure,
    use_container_width=True
)


# --------------------------------------------------
# PRIORITY ANALYSIS
# --------------------------------------------------

st.subheader("🎯 Customer Priority Analysis")

col1, col2 = st.columns(2)


with col1:

    priority_summary = (
        priority_data["priority"]
        .value_counts()
        .reset_index()
    )

    priority_summary.columns = [
        "priority",
        "customer_count"
    ]

    fig_priority = px.pie(
        priority_summary,
        names="priority",
        values="customer_count",
        title="Customer Priority Distribution"
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True
    )


with col2:

    ltv_summary = (
        ltv_predictions["ltv_segment"]
        .value_counts()
        .reset_index()
    )

    ltv_summary.columns = [
        "ltv_segment",
        "customer_count"
    ]

    fig_ltv = px.pie(
        ltv_summary,
        names="ltv_segment",
        values="customer_count",
        title="LTV Segment Distribution"
    )

    st.plotly_chart(
        fig_ltv,
        use_container_width=True
    )


# --------------------------------------------------
# CRITICAL CUSTOMERS
# --------------------------------------------------

st.subheader("🚨 Critical Customers")

critical_data = priority_data[
    priority_data["priority"]
    == "Critical - High Risk High Value"
].copy()

critical_data = critical_data.sort_values(
    by="predicted_ltv",
    ascending=False
)

st.dataframe(
    critical_data.head(20),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# HIGH RISK CUSTOMERS
# --------------------------------------------------

st.subheader("⚠️ Highest Churn Risk Customers")

risk_data = priority_data.sort_values(
    by="churn_probability",
    ascending=False
)

st.dataframe(
    risk_data.head(20),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# HIGH VALUE CUSTOMERS
# --------------------------------------------------

st.subheader("💰 Highest LTV Customers")

value_data = priority_data.sort_values(
    by="predicted_ltv",
    ascending=False
)

st.dataframe(
    value_data.head(20),
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# CUSTOMER PREDICTION
# --------------------------------------------------

st.divider()

st.subheader("🔮 Customer Churn & LTV Prediction")

st.write(
    "Enter customer information to predict churn risk, "
    "customer LTV and retention priority."
)

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12
    )

with col2:

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

with col3:

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )


col4, col5, col6 = st.columns(3)

with col4:

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

with col5:

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

with col6:

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )


col7, col8 = st.columns(2)

with col7:

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=1.0
    )

with col8:

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=840.0,
        step=1.0
    )


if st.button(
    "🔮 Predict Customer",
    type="primary"
):

    prediction_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:

        import requests

        response = requests.post(
            "http://127.0.0.1:8000/predict/priority",
            json=prediction_data,
            timeout=10
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction completed successfully!")

            st.divider()

            result_col1, result_col2, result_col3, result_col4, result_col5 = st.columns(5)

            with result_col1:
                st.metric(
                    "Churn Probability",
                    f"{result['churn_probability'] * 100:.2f}%"
                )

            with result_col2:
                churn_status = (
                    "Likely to Churn"
                    if result["predicted_churn"] == 1
                    else "Likely to Stay"
                )

                st.metric(
                    "Churn Prediction",
                    churn_status
                )

            with result_col3:
                st.metric(
                    "Predicted LTV",
                    f"${result['predicted_ltv']:,.2f}"
                )

            with result_col4:
                st.metric(
                    "LTV Segment",
                    result["ltv_segment"]
                )

            with result_col5:
                st.metric(
                    "Priority",
                    result["priority"]
                )

        else:

            st.error(
                f"Prediction failed. API returned status "
                f"{response.status_code}"
            )

            st.code(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure the FastAPI server is running."
        )

    except Exception as e:

        st.error("An error occurred during prediction.")

        st.code(str(e))

        
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Churn & LTV Prediction Engine | "
    "Python • PostgreSQL • Machine Learning • FastAPI • Streamlit"
)