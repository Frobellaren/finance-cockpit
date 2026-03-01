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


def top_expenses_by_description(
    df: pd.DataFrame,
    n: int = 20,
    exclude_categories: list[str] | None = None,
) -> pd.DataFrame:
    exclude_categories = exclude_categories or []

    data = df.copy()

    # 1) bara utgifter
    data = data[data["amount"] < 0]

    # 2) exkludera kategorier (kräver att df har 'category')
    if "category" in data.columns and exclude_categories:
        data = data[~data["category"].isin(exclude_categories)]

    # 3) summera per beskrivning
    data["spent"] = -data["amount"]
    top = (
        data.groupby("description")["spent"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    return top