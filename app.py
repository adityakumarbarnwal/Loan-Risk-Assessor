import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import kagglehub
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# Page Config
# =========================
st.set_page_config(page_title="Loan Default Dashboard", layout="wide")
st.title("💰 Loan Default Prediction Dashboard")
st.markdown("Interactive dashboard for **loan approval / default prediction** using **XGBoost**.")

# =========================
# Load Dataset
# =========================
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("algozee/credit-risk-and-loan-default-analysis-dataset")
    files = os.listdir(path)
    csv_file = [f for f in files if f.endswith(".csv")][0]
    file_path = os.path.join(path, csv_file)
    df = pd.read_csv(file_path)
    return df

df = load_data()

# =========================
# Load Model Files
# =========================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# =========================
# Basic Cleaning (for app visuals only)
# =========================
df = df.copy()

# Fill missing values for visualization
for col in df.columns:
    if df[col].dtype == "object":
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].median(), inplace=True)

# =========================
# Sidebar Inputs
# =========================
st.sidebar.header("📋 Enter Customer Details")

age = st.sidebar.slider("Age", 18, 70, 30)
income = st.sidebar.number_input("Income", value=50000.0)
loan_amount = st.sidebar.number_input("Loan Amount", value=20000.0)
credit_score = st.sidebar.slider("Credit Score", 300, 850, 650)
experience = st.sidebar.slider("Years of Experience", 0, 40, 5)

gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
education = st.sidebar.selectbox("Education", ["Bachelors", "High School", "Masters", "PhD"])
city = st.sidebar.selectbox("City", ["Chicago", "Houston", "San Fransisco", "New York"])
employment = st.sidebar.selectbox("Employment Type", ["Salaried", "Self-Employed","Unemployed"])

# =========================
# Create Input Dictionary
# =========================
input_data = {
    "Age": age,
    "Income": income,
    "LoanAmount": loan_amount,
    "CreditScore": credit_score,
    "YearsExperience": experience
}

for col in feature_columns:
    if col not in input_data:
        input_data[col] = 0

if f"Gender_{gender}" in feature_columns:
    input_data[f"Gender_{gender}"] = 1

if f"Education_{education}" in feature_columns:
    input_data[f"Education_{education}"] = 1

if f"City_{city}" in feature_columns:
    input_data[f"City_{city}"] = 1

if f"EmploymentType_{employment}" in feature_columns:
    input_data[f"EmploymentType_{employment}"] = 1

input_df = pd.DataFrame([input_data])
input_df = input_df[feature_columns]

# =========================
# Top Metrics
# =========================
st.subheader("📌 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Avg Income", f"{df['Income'].mean():,.0f}")
col4.metric("Avg Credit Score", f"{df['CreditScore'].mean():.0f}")

# =========================
# Prediction Section
# =========================
st.subheader("🔍 Loan Prediction")

if st.button("Predict Loan Default / Approval"):
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    c1, c2 = st.columns([1, 1])

    with c1:
        if prediction == 1:
            st.error(f"⚠️ High Risk / Not Approved")
        else:
            st.success(f"✅ Low Risk / Likely Approved")

    with c2:
        st.info(f"📊 Probability Score: {probability:.2%}")

    st.subheader("📄 Customer Input Summary")
    st.dataframe(pd.DataFrame({
        "Feature": ["Age", "Income", "LoanAmount", "CreditScore", "YearsExperience", "Gender", "Education", "City", "EmploymentType"],
        "Value": [age, income, loan_amount, credit_score, experience, gender, education, city, employment]
    }))

# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dataset", "📈 Visualizations", "🔥 Correlation", "⭐ Feature Importance", "👤 Compare User"
])

# =========================
# TAB 1: Dataset
# =========================
with tab1:
    st.subheader("Dataset Preview")
    st.dataframe(df.head(20))

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Values"}))

# =========================
# TAB 2: Visualizations
# =========================
with tab2:
    st.subheader("Interactive Visualizations")

    # Target Distribution
    if "LoanApproved" in df.columns:
        fig_target = px.histogram(
            df,
            x="LoanApproved",
            color="LoanApproved",
            title="Loan Approved Distribution"
        )
        st.plotly_chart(fig_target, use_container_width=True)

    # Income Distribution
    fig_income = px.histogram(
        df,
        x="Income",
        nbins=30,
        title="Income Distribution"
    )
    st.plotly_chart(fig_income, use_container_width=True)

    # Credit Score Distribution
    fig_credit = px.histogram(
        df,
        x="CreditScore",
        nbins=30,
        title="Credit Score Distribution"
    )
    st.plotly_chart(fig_credit, use_container_width=True)

    # Loan Amount by Education
    if "Education" in df.columns:
        fig_edu = px.box(
            df,
            x="Education",
            y="LoanAmount",
            color="Education",
            title="Loan Amount by Education"
        )
        st.plotly_chart(fig_edu, use_container_width=True)

    # City-wise Loan Amount
    if "City" in df.columns:
        fig_city = px.bar(
            df.groupby("City")["LoanAmount"].mean().reset_index(),
            x="City",
            y="LoanAmount",
            color="City",
            title="Average Loan Amount by City"
        )
        st.plotly_chart(fig_city, use_container_width=True)

# =========================
# TAB 3: Correlation Heatmap
# =========================
with tab3:
    st.subheader("Correlation Heatmap")

    numeric_df = df.select_dtypes(include=np.number)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# =========================
# TAB 4: Feature Importance
# =========================
with tab4:
    st.subheader("Top Feature Importance")

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": feature_columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        fig_imp = px.bar(
            importance_df.head(15),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Important Features"
        )
        st.plotly_chart(fig_imp, use_container_width=True)

        st.dataframe(importance_df.head(15))

# =========================
# TAB 5: Compare User with Dataset
# =========================
with tab5:
    st.subheader("Compare User Input with Dataset Average")

    compare_df = pd.DataFrame({
        "Feature": ["Age", "Income", "LoanAmount", "CreditScore", "YearsExperience"],
        "User Input": [age, income, loan_amount, credit_score, experience],
        "Dataset Average": [
            df["Age"].mean(),
            df["Income"].mean(),
            df["LoanAmount"].mean(),
            df["CreditScore"].mean(),
            df["YearsExperience"].mean()
        ]
    })

    st.dataframe(compare_df)

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        x=compare_df["Feature"],
        y=compare_df["User Input"],
        name="User Input"
    ))
    fig_compare.add_trace(go.Bar(
        x=compare_df["Feature"],
        y=compare_df["Dataset Average"],
        name="Dataset Average"
    ))

    fig_compare.update_layout(
        title="User Input vs Dataset Average",
        barmode="group"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

     # python -m streamlit run app.py  