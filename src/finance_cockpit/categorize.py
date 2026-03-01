import pandas as pd


RULES = [
    ("Mat", ["ICA", "COOP", "WILLYS", "HEMKÖP"]),
    ("Transport", ["SKÅNETRAFIKEN", "SL", "SJ", "UBER", "BOLT", "RYDE","CAR", "VOI"]),
    ("Räkningar", ["HYRA", "HSB", "EL","HEMFÖRSÄKR", "VATTEN","TELE2"]),
    ("Swish", ["SWISH"]),
    ("Överföring", ["DEPARTURES", "ARRIVALS"])
]


def categorize_transactions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["category"] = "Okänt"

    # Vi jobbar med versaler så matchning blir enklare
    desc = out["description"].astype(str).str.upper()

    # Gör om till "ord": byt allt som inte är bokstav/siffra mot mellanslag
    desc_tokens = desc.str.replace(r"[^A-ZÅÄÖ0-9]+", " ", regex=True)

# Lägg mellanslag i början/slutet så vi kan söka på " EL "
    desc_tokens = " " + desc_tokens + " "

    for category, keywords in RULES:
        mask = False
        for kw in keywords:
            mask = mask | desc_tokens.str.contains(f" {kw} ", regex=False)

        # bara sätt kategori där det fortfarande är Okänt
        out.loc[mask & (out["category"] == "Okänt"), "category"] = category


    return out
