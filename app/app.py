import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests

st.set_page_config(
    page_title="FraudShield",
    page_icon="🛡️",
    layout="wide"
)
# ================= Sidebar =================
#
with st.sidebar:

    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTlz_rhay7vAk9i0JmF_Amu7v4pwu8bUSRtpgBDNH-wQ&s=10",
        width=80
    )

    st.title("FraudShield")

    st.markdown("---")

    st.markdown("""
### Project Details

**Model**
- Random Forest

**Frontend**
- Streamlit

**Backend**
- FastAPI

**Language**
- Python

**Developer**
- Manish Saini
""")

    st.markdown("---")

    st.caption("Version 1.0")
st.title("🛡️ FraudShield")
st.markdown("### AI-Powered Credit Card Fraud Detection System")

st.divider()

# ================= MAIN LAYOUT ================= #

left_col, right_col = st.columns([2, 1])

# ==========================================================
# LEFT SIDE
# ==========================================================

with left_col:

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        merchant = st.text_input(
            "Merchant Name",
            placeholder="Enter Merchant Name"
        )

        category = st.selectbox(
            "Transaction Category",
            [
                "entertainment",
                "food_dining",
                "gas_transport",
                "grocery_net",
                "grocery_pos",
                "health_fitness",
                "home",
                "kids_pets",
                "misc_net",
                "misc_pos",
                "personal_care",
                "shopping_net",
                "shopping_pos",
                "travel"
            ]
        )

        transaction_hours = st.slider(
            "Transaction Hour",
            0,
            23,
            12
        )

        previous_avg_amt = st.number_input(
            "Previous Average Amount",
            min_value=0.0,
            value=100.0
        )

        amount_difference = st.number_input(
            "Amount Difference",
            value=0.0
        )

        transaction_day = st.slider(
            "Transaction Day",
            1,
            31,
            15
        )

        transaction_weekday = st.selectbox(
            "Transaction Weekday",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

    with input_col2:

        amount = st.number_input(
            "Transaction Amount ($)",
            min_value=0.0,
            step=1.0
        )

        age = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=100,
            value=30
        )

        merchant_distance = st.number_input(
            "Merchant Distance (km)",
            min_value=0.0,
            value=5.0
        )

        merchant_visit_frequency = st.number_input(
            "Merchant Visit Frequency",
            min_value=0,
            value=1
        )

        is_night_transaction = st.checkbox(
            "Night Transaction"
        )

        transaction_month = st.selectbox(
            "Transaction Month",
            list(range(1, 13))
        )

# ==========================================================
# RIGHT SIDE
# ==========================================================
with right_col:

    st.info("""
### 🛡️ FraudShield

Predict whether a credit card transaction is fraudulent using our trained Machine Learning model.

**Model**
- Random Forest

**Backend**
- FastAPI

**Status**
- 🟢 Ready
""")

    st.divider()

    predict_button = st.button(
        "🔍 Predict Fraud",
        use_container_width=True
    )

    if predict_button:

        input_data = {

            "merchant": merchant,
            "category": category,
            "amt": amount,
            "age": age,

            "transaction_hours": transaction_hours,
            "transaction_day": transaction_day,
            "transaction_month": transaction_month,
            "transaction_weekday": transaction_weekday,

            "is_night_transaction": is_night_transaction,

            "merchant_distance": merchant_distance,
            "previous_avg_amt": previous_avg_amt,
            "amount_difference": amount_difference,
            "merchant_visit_frequency": merchant_visit_frequency
        }

        try:

            with st.spinner("🔍 Analyzing Transaction..."):

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=input_data,
                    timeout=10
                )

                result = response.json()

            st.divider()

            if result["prediction"] == "Fraud":

                st.error("🚨 Fraud Transaction Detected")

            else:

                st.success("✅ Legitimate Transaction")

            st.metric(
                label="Fraud Probability",
                value=f"{result['fraud_probability']:.2%}"
            )

            st.progress(result["fraud_probability"])

            if result["fraud_probability"] >= 0.70:

                st.warning("⚠ Risk Level : HIGH")

            elif result["fraud_probability"] >= 0.40:

                st.info("🟡 Risk Level : MEDIUM")

            else:

                st.success("🟢 Risk Level : LOW")

        except Exception:

            st.error(
                "⚠ Unable to connect to FastAPI Backend.\n\nPlease make sure FastAPI server is running."
            )

st.divider()

st.caption(
    "🛡️ FraudShield | AI Powered Credit Card Fraud Detection | Developed by Manish Saini | Version 1.0"
)