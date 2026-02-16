import pandas as pd


RULES = [
    ("Mat", ["ICA", "COOP", "WILLYS", "HEMKÖP"]),
    ("Transport", ["SKÅNETRAFIKEN", "SL", "SJ", "UBER", "BOLT", "RYDE","CAR", "VOI"]),
    ("Boende", ["HYRA", "HSB", "HEMFÖRSÄKR", "EL", "VATTEN"]),
    ("Swish", ["SWISH"]),
    ("Överföring", ["DEPARTURES", "ARRIVALS"])
]


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["category"] = "Okänt"

    # Vi jobbar med versaler så matchning blir enklare
    desc = out["description"].astype(str).str.upper()

    for category, keywords in RULES:
        mask = False
        for kw in keywords:
            mask = mask | desc.str.contains(kw, regex=False)

        # bara sätt kategori där det fortfarande är Okänt
        out.loc[mask & (out["category"] == "Okänt"), "category"] = category


    return out
