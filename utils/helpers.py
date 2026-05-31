import streamlit as st
import pandas as pd

def render_glass_table(df):

    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            df[col] = df[col].astype(str)

    if len(df) >= 10:
        height = 350
    else:
        height = (len(df) + 1) * 40

    st.markdown(
        '<div class="glass-table">',
        unsafe_allow_html=True
    )

    st.dataframe(
        df,
        height=height,
        width="stretch"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )