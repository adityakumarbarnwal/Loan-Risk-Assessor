
import streamlit as st
import pandas as pd
import plotly.express as px
from pyexpat import model

from utils.helpers import render_glass_table

def render(df,pipeline,model):
    st.markdown('<div class="section-header">🧠 Model Workflow (XGBoost Pipeline)</div>', unsafe_allow_html=True)

    st.markdown("### 1️⃣ Data Input")
    st.write("""
    - Raw dataset contains numerical + categorical features
    - Examples:
        - Numerical: Age, Income, LoanAmount, CreditScore
        - Categorical: Gender, Education, City, EmploymentType
    """)

    render_glass_table(df.head(10))

    st.markdown("### 2️⃣ Data Preprocessing")

    st.write("""
    - Missing values handled:
        - Numerical → Median
        - Categorical → Mode
    - Ensures no null values during training
    """)

    missing_after = df.isnull().sum().sum()
    st.metric("Missing Values After Cleaning", missing_after)

    st.markdown("### 3️⃣ Feature Encoding")
    # Extract preprocessor from pipeline
    preprocessor = pipeline.named_steps["preprocessor"]

    # Extract StandardScaler (numerical transformer)
    scaler = preprocessor.named_transformers_["num"]
    numeric_cols = ["Age", "Income", "LoanAmount", "CreditScore", "YearsExperience"]

    st.write("""
    - One-Hot Encoding applied on categorical variables
    - Example:
        - Gender → Gender_Male, Gender_Female
        - City → City_NewYork, City_Houston, etc.
    """)
    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    sample_features = pd.DataFrame(feature_names, columns=["Encoded Features"])
    render_glass_table(sample_features.head(15))

    st.markdown("### 4️⃣ Feature Scaling")

    st.write("""
    - StandardScaler applied on numerical features
    - Formula:
        z = (x - mean) / std
    """)

    numeric_cols = ["Age", "Income", "LoanAmount", "CreditScore", "YearsExperience"]

    sample_numeric = df[numeric_cols].head(5)
    scaled_sample = scaler.transform(sample_numeric)
    scaled_df = pd.DataFrame(scaled_sample, columns=numeric_cols)

    st.markdown("#### 🔹 Before Scaling")
    render_glass_table(sample_numeric)

    st.markdown("#### 🔹 After Scaling")
    render_glass_table(scaled_df)

    st.info("StandardScaler is applied only to numerical features inside the pipeline.")

    st.markdown("### 5️⃣ Model: XGBoost")
    st.write("""
    - Algorithm: Gradient Boosting (XGBoost)
    - Works by:
        1. Building decision trees sequentially
        2. Each tree corrects previous errors
        3. Final output = weighted sum of trees

    - Advantages:
        - Handles non-linearity
        - High accuracy
        - Built-in feature importance
    """)

    if hasattr(model, "feature_importances_"):
        feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })

        def map_feature(name):
            if "__" in name:
                name = name.split("__")[1]
            return name.split("_")[0]

        importance_df["Feature"] = importance_df["Feature"].apply(map_feature)

        importance_df = (
            importance_df
            .groupby("Feature")["Importance"]
            .sum()
            .reset_index()
            .sort_values(by="Importance", ascending=False)
            .head(10)
        )
        fig_imp = px.bar(
            importance_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top Features Used by XGBoost"
        )
        st.plotly_chart(fig_imp, width='stretch')

    st.markdown("### 6️⃣ Prediction Pipeline Flow")

    st.write("""
    **Step-by-step flow inside app:**
    """)

    flow_df = pd.DataFrame({
        "Step": [
            "User Input",
            "Convert to DataFrame",
            "Pipeline Preprocessing",
            "Encoding + Scaling",
            "Model Prediction",
            "Probability Output"
        ],
        "Description": [
            "User enters details from sidebar",
            "Converted into structured input_df",
            "Pipeline applies preprocessing",
            "OneHotEncoding + StandardScaler applied",
            "Passed into XGBoost model",
            "Returns risk probability"
        ]
    })

    render_glass_table(flow_df)

    st.markdown("### 7️⃣ Final Output Interpretation")

    st.write("""
    - Model outputs:
        - Probability of Default
        - Probability of Approval
    - Based on threshold:
        - High Risk
        - Medium Risk
        - Low Risk
    """)

    st.success("✔️ This pipeline ensures consistent preprocessing and accurate predictions.")
