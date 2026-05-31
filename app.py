from utils.model_loader import load_pipeline
from utils.data_loader import load_data
from utils.helpers import render_glass_table
from tabs.eda_tab import render as eda_tab
from tabs.visualization_tab import render as visualization_tab
from tabs.correlation_tab import render as correlation_tab
from tabs.feature_importance_tab import render as feature_importance_tab
from tabs.compare_user_tab import render as compare_user_tab
from tabs.metrics_tab import render as metrics_tab
from tabs.workflow_tab import render as workflow_tab
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

def load_css():
    with open("styles/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# Page Config

st.set_page_config(page_title="Loan Default Dashboard", layout="wide")

load_css()

st.markdown('<div class="title">💰 Loan Default Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Loan risk intelligence system</div>', unsafe_allow_html=True)

# Loading Dataset
if not os.path.exists("loan_risk_prediction_dataset.csv"):
    st.error("Dataset file missing. Please add it to the project folder.")
    st.stop()

df = load_data()
pipeline = load_pipeline()
model = pipeline.named_steps["model"]

# Basic Cleaning (for app visuals only)
df = df.copy()

# Fill missing values for visualization
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

# Sidebar Inputs

st.sidebar.markdown("## ⚙️ Customer Profile")
st.sidebar.markdown("---")

age = st.sidebar.slider("Age", 18, 70, 30)
income = st.sidebar.number_input("Income", value=50000.0)
loan_amount = st.sidebar.number_input("Loan Amount", value=20000.0)
credit_score = st.sidebar.slider("Credit Score", 300, 850, 650)
experience = st.sidebar.slider("Years of Experience", 0, 40, 5)

gender = st.sidebar.selectbox("Gender", ["Female", "Male"])
education = st.sidebar.selectbox("Education", ["Bachelors", "High School", "Masters", "PhD"])
city = st.sidebar.selectbox("City", ["Chicago", "Houston", "San Francisco", "New York"])
employment = st.sidebar.selectbox("Employment Type", ["Salaried", "Self-Employed","Unemployed"])

# Create Input Dictionary

input_df = pd.DataFrame([{
    "Age": age,
    "Income": income,
    "LoanAmount": loan_amount,
    "CreditScore": credit_score,
    "YearsExperience": experience,
    "Gender": gender,
    "Education": education,
    "City": city,
    "EmploymentType": employment
}])
# Top Metrics

st.markdown('<div class="section-header">📌 Dataset Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-value">{df.shape[0]}</div>
        <div class="metric-label">TOTAL RECORDS</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📦</div>
        <div class="metric-value">{df.shape[1]}</div>
        <div class="metric-label">COLUMNS</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-value">{int(df['Income'].mean()):,}</div>
        <div class="metric-label">AVG INCOME</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">⭐</div>
        <div class="metric-value">{int(df['CreditScore'].mean())}</div>
        <div class="metric-label">AVG CREDIT SCORE</div>
    </div>
    """, unsafe_allow_html=True)

# Prediction Section
st.markdown('<div class="section-header">🔍 Loan Prediction</div>', unsafe_allow_html=True)

if st.button("🔮 Predict Risk"):
    prediction = pipeline.predict(input_df)[0]

    probs = pipeline.predict_proba(input_df)[0]
    prob_approved = probs[1]
    prob_default = probs[0]

    # Result Card(Open)
    st.divider()
    st.markdown('<div class="glass result-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    # Left
    with col1:
        if prediction == 0:
            st.markdown("### ❌ High Risk Applicant")
            st.markdown(f"**Default Probability:** `{prob_default:.2%}`")
        else:
            st.markdown("### ✅ Low Risk Applicant")
            st.markdown(f"**Approval Probability:** `{prob_approved:.2%}`")

    # Middle
    with col2:
        risk_score = int(prob_default * 100)
        st.metric("Risk Score", f"{risk_score}%")

    # Right
    with col3:
        if prob_default > 0.7:
            st.markdown("🔴 **High Risk**")
        elif prob_default > 0.4:
            st.markdown("🟠 **Medium Risk**")
        else:
            st.markdown("🟢 **Low Risk**")

    st.progress(int(prob_default * 100))

    # Feature Section
    if hasattr(model, "feature_importances_"):
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📌 Key Influencing Factors</div>', unsafe_allow_html=True)

        # Get feature names AFTER preprocessing
        feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })

        # Converting encoded → original feature
        def map_feature(name):
            if "__" in name:
                name = name.split("__")[1]
            return name.split("_")[0]

        importance_df["Feature"] = importance_df["Feature"].apply(map_feature)

        # Grouping
        importance_df = (
            importance_df
            .groupby("Feature")["Importance"]
            .sum()
            .reset_index()
            .sort_values(by="Importance", ascending=False)
        )

        top_features = importance_df.head(3)

        styled_top = (
            top_features.style
            .bar(subset=["Importance"], color="#22c55e")
            .format({"Importance": "{:.4f}"})
            .set_properties(**{"color": "white"})
        )

        st.markdown('<div class="glass-table">', unsafe_allow_html=True)
        st.markdown(styled_top.to_html(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Close Feature Section
        st.markdown('</div>', unsafe_allow_html=True)

    # Summary Section
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📄 Customer Input Summary</div>', unsafe_allow_html=True)

    summary_df = pd.DataFrame({
        "Feature": ["Age", "Income", "LoanAmount", "CreditScore", "YearsExperience", "Gender", "Education", "City", "EmploymentType"],
        "Value": [age, income, loan_amount, credit_score, experience, gender, education, city, employment]
    })

    render_glass_table(summary_df, cmap="Blues")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 EDA", "📈 Visualizations", "🔥 Correlation",
    "⭐ Feature Importance", "👤 Compare User",
    "📊 Metrics", "🧠 Model Workflow"
])


with tab1:
    eda_tab(df)

with tab2:
    visualization_tab(df)

with tab3:
    correlation_tab(df)

with tab4:
    feature_importance_tab(df, pipeline, model)

with tab5:
    compare_user_tab(df, age, income, loan_amount, credit_score, experience)

with tab6:
    metrics_tab(df)

with tab7:
    workflow_tab(df, pipeline, model)
     # python -m streamlit run app.py