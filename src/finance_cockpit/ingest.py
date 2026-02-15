import pandas as pd


def read_csv_file(file) -> pd.DataFrame:
    df = pd.read_csv(file, encoding="cp1252", sep=";")

    return df

