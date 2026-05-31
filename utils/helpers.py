import streamlit as st
def render_glass_table(df, cmap="viridis"):
    if len(df) >= 10:
        height = 350
    else:
        height = (len(df) + 1) * 40

    styled_df = df.style.background_gradient(cmap=cmap)

    st.markdown(
        '<div class="glass-table">',
        unsafe_allow_html=True
    )

    st.dataframe( df,height=height,width='stretch')
    st.markdown('</div>',unsafe_allow_html=True)