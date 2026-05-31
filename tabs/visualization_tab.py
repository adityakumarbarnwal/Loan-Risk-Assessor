import streamlit as st
import plotly.express as px

def render(df):
    st.markdown('<div class="section-header">📈 Visualizations</div>', unsafe_allow_html=True)

    # Target Distribution
    if "LoanApproved" in df.columns:
        fig_target = px.histogram(
            df,
            x="LoanApproved",
            color="LoanApproved",
            title="Loan Approved Distribution"
        )
        st.plotly_chart(fig_target, width='stretch')

    # Income Distribution
    fig_income = px.histogram(
        df,
        x="Income",
        nbins=30,
        title="Income Distribution"
    )
    st.plotly_chart(fig_income, width='stretch')

    # Credit Score Distribution
    fig_credit = px.histogram(
        df,
        x="CreditScore",
        nbins=30,
        title="Credit Score Distribution"
    )
    st.plotly_chart(fig_credit, width='stretch')

    # Loan Amount by Education
    if "Education" in df.columns:
        fig_edu = px.box(
            df,
            x="Education",
            y="LoanAmount",
            color="Education",
            title="Loan Amount by Education"
        )
        st.plotly_chart(fig_edu, width='stretch')

    # City-wise Loan Amount
    if "City" in df.columns:
        fig_city = px.bar(
            df.groupby("City")["LoanAmount"].mean().reset_index(),
            x="City",
            y="LoanAmount",
            color="City",
            title="Average Loan Amount by City"
        )
        st.plotly_chart(fig_city, width='stretch')

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
        col1.plotly_chart(fig_pie1, width='stretch')

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
        col2.plotly_chart(fig_pie2, width='stretch')

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
        st.plotly_chart(fig_pie3, width='stretch')

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
        st.plotly_chart(fig_pie4, width='stretch')