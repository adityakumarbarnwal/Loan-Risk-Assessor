
import streamlit as st


def render(df):
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
