import joblib
import streamlit as st


@st.cache_resource
def load_pipeline():
    return joblib.load("pipeline.pkl")