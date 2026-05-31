import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import render_glass_table

def render(df,pipeline,model):
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
        st.plotly_chart(fig_imp)
        render_glass_table(importance_df.head(15))