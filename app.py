import streamlit as st
import pandas as pd

st.title("Finance Cockpit")

st.write("Första versionen av min privatekonomi-app")

#Dummy-data

data = {
    "month" : ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun"],
    "income" : [13500,13500,13500,13500,13500,13500],
    "expenses" : [10000,10000,10000,10000,10000,10000]
}

df = pd.DataFrame(data)
df["savings"] = df["income"] - df["expenses"]

st.subheader("Månadsdata")
st.dataframe(df)

st.subheader("Sparande över tid")
st.line_chart(df.set_index("month")["savings"])