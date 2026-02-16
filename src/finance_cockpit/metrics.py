import pandas as pd


def monthly_summary(df:pd.DataFrame) -> pd.DataFrame:

    data = df.copy()

    data["month"] = data["date"].dt.to_period("M")
    net = data.groupby("month")["amount"].sum()
    income = data[data["amount"] > 0].groupby("month")["amount"].sum()
    expenses = data[data["amount"] < 0].groupby("month")["amount"].sum()

    summary = pd.DataFrame({
        "income": income,
        "expenses": expenses,
        "net": net
    })

    summary = summary.fillna(0)

    summary.index = summary.index.astype(str)


    summary = summary.sort_index()
    return summary

def create_dummy_monthly_overview() -> pd.DataFrame:
    """Temporary data until we plug in real bank CSV."""
    data = {
        "month": ["Jan", "Feb", "Mar", "Apr", "Maj", "Jun"],
        "income": [25000, 25000, 25000, 25000, 25000, 25000],
        "expenses": [18000, 19000, 17500, 20000, 18500, 21000],
    }
    df = pd.DataFrame(data)
    df["savings"] = df["income"] - df["expenses"]
    return df



def monthly_category_pivot(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["month"] = data["date"].dt.to_period("M").astype(str)

    pivot = data.pivot_table(
        index="month",
        columns="category",
        values="amount",
        aggfunc="sum",
        fill_value=0.0,
    )

    return pivot
