import pandas as pd


def normalize_transactions(df: pd.DataFrame, date_col: str, desc_col: str, amount_col: str) -> pd.DataFrame:
    out = df[[date_col, desc_col, amount_col]].copy()
    out.columns = ["date", "description", "amount"]

    # date -> datetime
    out["date"] = pd.to_datetime(out["date"], errors="coerce")

    # description -> str
    out["description"] = out["description"].astype(str).str.strip()

    # amount: "1 234,56" -> 1234.56
    amt = out["amount"].astype(str)
    amt = amt.str.replace(" ", "", regex=False)
    amt = amt.str.replace(",", ".", regex=False)
    out["amount"] = pd.to_numeric(amt, errors="coerce")

    # clean up
    out = out.dropna(subset=["date", "amount"]).sort_values("date").reset_index(drop=True)
    return out
