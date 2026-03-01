import streamlit as st
from src.finance_cockpit.ingest import read_csv_file
from src.finance_cockpit.normalize import normalize_transactions
from src.finance_cockpit.metrics import monthly_summary,monthly_category_pivot, top_expenses_by_description
from src.finance_cockpit.categorize import categorize_transactions




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

def default_index(cols: list[str], preferred: list[str], fallback: int) -> int:
    for name in preferred:
        if name in cols:
            return cols.index(name)
    return min(fallback, len(cols) - 1)

date_col = st.selectbox("Datumkolumn", columns, index=default_index(columns, ["Bokföringsdag", "Datum"], 0))
desc_col = st.selectbox("Beskrivning", columns, index=default_index(columns, ["Specifikation", "Text"], 1))
amount_col = st.selectbox("Belopp", columns, index=default_index(columns, ["Belopp", "Amount"], 2))


normalized = normalize_transactions(df, date_col, desc_col, amount_col)

categorized = categorize_transactions(normalized)

# --- Sanity check ---
st.subheader("Översikt")
col1, col2 = st.columns(2)
with col1:
    st.metric("Antal transaktioner", len(categorized))
with col2:
    st.metric("Total netto", round(float(categorized["amount"].sum()), 2))



st.subheader("Transaktioner med kategori")
st.dataframe(categorized.head(100), use_container_width=True)


st.subheader("Summa per kategori")
by_cat = categorized.groupby("category")["amount"].sum().sort_values()
st.dataframe(by_cat)


pivot = monthly_category_pivot(categorized)

st.subheader("Månad × kategori")
st.dataframe(pivot, use_container_width=True)


monthly = monthly_summary(categorized)

st.subheader("Månadsöversikt")
st.dataframe(monthly)

st.subheader("Netto per månad")
st.line_chart(monthly["net"])

st.subheader("Topplista")

all_categories = sorted(categorized["category"].unique().tolist())

exclude = st.multiselect(
    "Exkludera kategorier",
    options=all_categories,
    default=[c for c in ["Swish", "Överföring"] if c in all_categories],
)

top = top_expenses_by_description(categorized, n=20, exclude_categories=exclude)

st.subheader("Top 20 utgifter (per beskrivning)")
st.dataframe(top, use_container_width=True)
st.bar_chart(top.set_index("description")["spent"])
