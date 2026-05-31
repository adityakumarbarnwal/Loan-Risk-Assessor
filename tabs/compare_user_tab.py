import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from utils.helpers import render_glass_table

def render(df, age, income, loan_amount, credit_score, experience):
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

    render_glass_table(compare_df)
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

    st.plotly_chart(fig_compare, width='stretch')