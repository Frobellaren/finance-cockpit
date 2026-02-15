import streamlit as st
from src.finance_cockpit.ingest import read_csv_file
from src.finance_cockpit.normalize import normalize_transactions


st.title("Finance Cockpit")

uploaded = st.file_uploader("Ladda upp bank-CSV", type=["csv", "txt"])

if uploaded is None:
    st.info("Välj en fil för att fortsätta.")
    st.stop()

try:
    df = read_csv_file(uploaded)

except Exception as e:
    st.error("Kunde inte läsa filen som CSV.")
    st.exception(e)
    st.stop()

st.dataframe(df.head(50), use_container_width=True)

st.subheader("Välj kolumner")

columns = df.columns.tolist()
date_col = st.selectbox("Datumkolumn", columns)
desc_col = st.selectbox("Beskrivning", columns)
amount_col = st.selectbox("Belopp", columns)

normalized = normalize_transactions(df, date_col, desc_col, amount_col)

st.subheader("Normaliserade transaktioner")
st.dataframe(normalized.head(50), use_container_width=True)

