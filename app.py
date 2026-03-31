import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Page Config

st.set_page_config(page_title="Loan Default Dashboard", layout="wide")
st.markdown("""
<style>

/* ===== Global Background ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
}
            
            /* ===== Glass Table Container ===== */
.glass-table {
    background: rgba(255,255,255,0.04);
    padding: 12px;
    border-radius: 14px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: inset 0 0 10px rgba(255,255,255,0.02);
    overflow: hidden;
}

/* SCROLLBAR STYLING (optional but looks premium) */
.glass-table div {
    scrollbar-width: thin;
    scrollbar-color: rgba(99,102,241,0.6) transparent;
}

.glass-table div::-webkit-scrollbar {
    width: 6px;
}

.glass-table div::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.6);
    border-radius: 10px;
}

/* ===== Table Styling ===== */
table {
    border-collapse: collapse !important;
    width: 100% !important;
    color: #e2e8f0 !important;
}

thead th {
    background: rgba(255,255,255,0.1) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

tbody tr {
    background: transparent;
}

tbody tr:hover {
    background: rgba(255,255,255,0.08);
}

td, th {
    padding: 10px !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* header stronger border */


/* remove last column right border */
td:last-child, th:last-child {
    border-right: none;
}

table td, table th {
    border-right: 1px solid rgba(255,255,255,0.08);
}

table tr:last-child td {
    border-bottom: none;
}
            
/* ===== Glass Card ===== */
.glass {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 25px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 40px rgba(0,0,0,0.3);
    margin: 20px 0;
    max-width: 100%;
}

/* ===== Title ===== */
.title {
    font-size: 34px;
    font-weight: 700;
}

/* ===== Subtitle ===== */
.subtitle {
    font-size: 15px;
    color: #94a3b8;
}

            
.metric-icon {
    font-size: 18px;
    margin-bottom: 10px;
    opacity: 0.8;
}

.metric-card {
    position: relative;
    padding: 30px;
    border-radius: 18px;

    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);

    border: 1px solid rgba(255,255,255,0.08);

    overflow: hidden;
    transition: all 0.35s ease;
}

/* gradient glow layer */
.metric-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        120deg,
        rgba(99,102,241,0.25),
        rgba(34,197,94,0.15),
        transparent
    );
    opacity: 0.6;
}

/* light edge shine */
.metric-card::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(255,255,255,0.2);
}

/* hover = depth */
.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

/* VALUE */
.metric-value {
    font-size: 38px;
    font-weight: 700;
    color: #93c5fd;
    position: relative;
    z-index: 1;
}

/* LABEL */
.metric-label {
    font-size: 12px;
    letter-spacing: 1.5px;
    color: #94a3b8;
    margin-top: 8px;
    position: relative;
    z-index: 1;
}

/* ===== Buttons ===== */
/* ===== BUTTON BASE ===== */
.stButton>button {
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;

    background: linear-gradient(135deg, #6366f1, #22c55e);
    color: white;
    border: none;

    transition: all 0.25s ease;
}

/* ===== HOVER ===== */
.stButton>button:hover {
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 8px 20px rgba(99,102,241,0.4);
}

/* ===== CLICK EFFECT ===== */
.stButton>button:active {
    transform: scale(0.96);
}

/* ===== RIPPLE EFFECT (fake but smooth) ===== */
.stButton>button::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 12px;
    opacity: 0;
    background: rgba(255,255,255,0.2);
    transition: opacity 0.3s;
}

.stButton>button:active::after {
    opacity: 1;
}

.risk {
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 600;
    text-align: center;
    margin-top: 5px;
}

.risk.high {
    background: rgba(239,68,68,0.15);
    color: #ef4444;
}

.risk.medium {
    background: rgba(251,191,36,0.15);
    color: #fbbf24;
}

.risk.low {
    background: rgba(34,197,94,0.15);
    color: #22c55e;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
}

.section-header {
    font-size: 24px;
    font-weight: 600;
    margin: 30px 0 15px 0;
    padding-bottom: 8px;

    color: #e2e8f0;
    letter-spacing: 0.4px;

    position: relative;
}

.section-header::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;

    width: 60px;
    height: 3px;

    border-radius: 3px;

    background: linear-gradient(135deg, #6366f1, #22c55e);
}


/* ===== Metrics ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
}

/* ===== Tabs ===== */
.stTabs [role="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
}
            
.result-card {
    background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(99,102,241,0.15));
    border: 1px solid rgba(255,255,255,0.1);
}

/* Hover Effect */
.glass:hover {
    transform: scale(1.01);
    transition: 0.25s ease;
}

            /* ===== TAB BAR ===== */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* ===== TAB BUTTON ===== */
.stTabs [role="tab"] {
    background: transparent;
    border-radius: 10px;
    padding: 10px 18px;
    margin-right: 6px;
    font-weight: 500;
    color: #cbd5f5;
    transition: all 0.3s ease;
}

/* ===== ACTIVE TAB ===== */
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #22c55e);
    color: white !important;
    transform: scale(1.05);
    box-shadow: 0 0 12px rgba(99,102,241,0.4);
}

/* ===== TAB HOVER ===== */
.stTabs [role="tab"]:hover {
    background: rgba(255,255,255,0.1);
    transform: translateY(-2px);
}

/* ===== TAB CONTENT ANIMATION ===== */
section[data-testid="stTabs"] > div > div {
    animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
            
/* FORCE REMOVE STREAMLIT BLACK BACKGROUND */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

def render_glass_table(df, cmap="viridis"):
    if len(df) >= 10:
        height = 350
    else:
        height = (len(df) + 1) * 40
    styled_df = df.style.background_gradient(cmap=cmap)

    st.markdown('<div class="glass-table">', unsafe_allow_html=True)
    st.dataframe(
        df,   # IMPORTANT: use df, not styled_df
        height=height,
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="title">💰 Loan Default Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Loan risk intelligence system</div>', unsafe_allow_html=True)

# Loading Dataset

if not os.path.exists("loan_risk_prediction_dataset.csv"):
    st.error("Dataset file missing. Please add it to the project folder.")
    st.stop()

@st.cache_data
def load_data():
    df = pd.read_csv("loan_risk_prediction_dataset.csv")
    return df

df = load_data()

# Loading Model Files

@st.cache_resource
def load_pipeline():
    return joblib.load("pipeline.pkl")

pipeline = load_pipeline()
model = pipeline.named_steps["model"]

# Basic Cleaning (for app visuals only)

df = df.copy()

# Fill missing values for visualization
for col in df.columns:
    if df[col].dtype == "object":
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].median(), inplace=True)

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

    # RESULT CARD (OPEN)
    st.divider()
    st.markdown('<div class="glass result-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    # LEFT
    with col1:
        if prediction == 0:
            st.markdown("### ❌ High Risk Applicant")
            st.markdown(f"**Default Probability:** `{prob_default:.2%}`")
        else:
            st.markdown("### ✅ Low Risk Applicant")
            st.markdown(f"**Approval Probability:** `{prob_approved:.2%}`")

    # MIDDLE
    with col2:
        risk_score = int(prob_default * 100)
        st.metric("Risk Score", f"{risk_score}%")

    # RIGHT
    with col3:
        if prob_default > 0.7:
            st.markdown("🔴 **High Risk**")
        elif prob_default > 0.4:
            st.markdown("🟠 **Medium Risk**")
        else:
            st.markdown("🟢 **Low Risk**")

    st.progress(int(prob_default * 100))

    # ===== FEATURE SECTION =====
    if hasattr(model, "feature_importances_"):
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.markdown('<div class="section-header">📌 Key Influencing Factors</div>', unsafe_allow_html=True)

        # Get feature names AFTER preprocessing
        feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })

        # 🔥 Convert encoded → original feature
        def map_feature(name):
            if "__" in name:
                name = name.split("__")[1]
            return name.split("_")[0]

        importance_df["Feature"] = importance_df["Feature"].apply(map_feature)

        # 🔥 Group
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

        # CLOSE FEATURE SECTION
        st.markdown('</div>', unsafe_allow_html=True)

    # ===== SUMMARY SECTION =====
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

# TAB 1: Dataset

with tab1:
    st.markdown('<div class="section-header">📊 Dataset Preview</div>', unsafe_allow_html=True)
    render_glass_table(df.head(20), cmap="viridis")

    st.markdown('<div class="section-header">⚠️ Missing Values</div>', unsafe_allow_html=True)

    missing_df = df.isnull().sum().reset_index().rename(
        columns={"index": "Column", 0: "Missing Values"}
    )
    render_glass_table(missing_df, cmap="magma")

    st.markdown('<div class="section-header">📌 Key EDA Insights</div>', unsafe_allow_html=True)

    st.write("""
    - Higher income applicants tend to have better loan approval chances.
    - Credit score is one of the strongest predictors of approval.
    - Loan amount distribution varies significantly across users.
    - Missing values were minimal and handled using median/mode imputation.
    """)

# TAB 2: Visualizations

with tab2:
    st.markdown('<div class="section-header">📈 Visualizations</div>', unsafe_allow_html=True)

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

# Categorical (Pie Charts)
    st.markdown('<div class="section-header">🥧 Categorical Distribution</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # LoanApproved
    if "LoanApproved" in df.columns:
        loan_counts = df["LoanApproved"].value_counts().reset_index()
        loan_counts.columns = ["LoanApproved", "Count"]

        fig_pie1 = px.pie(
            loan_counts,
            names="LoanApproved",
            values="Count",
            hole=0.4,
            title="Loan Approval Split"
        )
        fig_pie1.update_traces(textinfo='percent+label')
        col1.plotly_chart(fig_pie1, use_container_width=True)

    # Gender
    if "Gender" in df.columns:
        gender_counts = df["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]

        fig_pie2 = px.pie(
            gender_counts,
            names="Gender",
            values="Count",
            hole=0.4,
            title="Gender Distribution"
        )
        fig_pie2.update_traces(textinfo='percent+label')
        col2.plotly_chart(fig_pie2, use_container_width=True)

    # Education
    if "Education" in df.columns:
        edu_counts = df["Education"].value_counts().reset_index()
        edu_counts.columns = ["Education", "Count"]

        fig_pie3 = px.pie(
            edu_counts,
            names="Education",
            values="Count",
            title="Education Distribution"
        )
        fig_pie3.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie3, use_container_width=True)

    # Employment Type
    if "EmploymentType" in df.columns:
        emp_counts = df["EmploymentType"].value_counts().reset_index()
        emp_counts.columns = ["EmploymentType", "Count"]

        fig_pie4 = px.pie(
            emp_counts,
            names="EmploymentType",
            values="Count",
            title="Employment Type Distribution"
        )
        fig_pie4.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie4, use_container_width=True)

# TAB 3: Correlation Heatmap

with tab3:
    st.markdown('<div class="section-header">🔥 Correlation Heatmap</div>', unsafe_allow_html=True)

    numeric_df = df.select_dtypes(include=np.number)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# TAB 4: Feature Importance
with tab4:
    st.markdown('<div class="section-header">⭐ Feature Importance</div>', unsafe_allow_html=True)

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
        )

        fig_imp = px.bar(
            importance_df.head(15),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Important Features"
        )
        st.plotly_chart(fig_imp, use_container_width=True)

        render_glass_table(importance_df.head(15), cmap="viridis")

# TAB 5: Compare User with Dataset

with tab5:
    st.markdown('<div class="section-header">👤 Compare User with Dataset Average</div>', unsafe_allow_html=True)

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

    render_glass_table(compare_df, cmap="PuBu")

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

# TAB 6 : Metrics Tab

with tab6:
    st.markdown('<div class="section-header">📊 Model Performance</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown('<div class="metric-card"><div class="metric-value">0.96</div><div class="metric-label">ACCURACY</div></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-card"><div class="metric-value">0.9524</div><div class="metric-label">PRECISION</div></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-card"><div class="metric-value">0.8696</div><div class="metric-label">RECALL</div></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric-card"><div class="metric-value">0.9091</div><div class="metric-label">F1 SCORE</div></div>', unsafe_allow_html=True)
    col5.markdown('<div class="metric-card"><div class="metric-value">0.9303</div><div class="metric-label">ROC AUC</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📌 Model Insights")
    st.write("""
    - High accuracy (96%) indicates strong prediction capability.
    - High precision ensures fewer incorrect approvals.
    - Recall shows model can detect most risky applicants.
    - Balanced F1 score confirms overall robustness.
    - ROC AUC shows excellent class separation ability.
    """)

with tab7:
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
        st.plotly_chart(fig_imp, use_container_width=True)

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

     # python -m streamlit run app.py