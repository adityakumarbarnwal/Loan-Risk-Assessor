import streamlit as st
import pandas as pd
from utils.helpers import render_glass_table


def render(df):
    st.markdown(
        '<div class="section-header">📊 Dataset Preview</div>',
        unsafe_allow_html=True
    )

    render_glass_table(df.head(20))

    st.markdown(
        '<div class="section-header">⚠️ Missing Values</div>',
        unsafe_allow_html=True
    )

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
        .rename(
            columns={
                "index": "Column",
                0: "Missing Values"
            }
        )
    )

    render_glass_table(missing_df)

    st.markdown(
        '<div class="section-header">📌 Key EDA Insights</div>',
        unsafe_allow_html=True
    )

    st.write("""
    - Higher income applicants tend to have better approval chances.
    - Credit score strongly impacts approval.
    - Loan amount varies across applicants.
    - Missing values handled using median/mode imputation.
    """)