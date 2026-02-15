import streamlit as st
from src.finance_cockpit.metrics import create_dummy_monthly_overview

st.title("Finance Cockpit")

df = create_dummy_monthly_overview()

st.subheader("Månadsdata")
st.dataframe(df, use_container_width=True)

st.subheader("Sparande över tid")
st.line_chart(df.set_index("month")["savings"])

