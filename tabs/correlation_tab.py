import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def render(df):
    st.markdown(
        '<div class="section-header">🔥 Correlation Heatmap</div>',
        unsafe_allow_html=True
    )

    numeric_df = df.select_dtypes(include=np.number)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)