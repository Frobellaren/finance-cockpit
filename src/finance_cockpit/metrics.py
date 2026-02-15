import pandas as pd


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
