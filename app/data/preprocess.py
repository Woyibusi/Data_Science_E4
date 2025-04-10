# preprocess.py

import pandas as pd

def clean_series(df):
    if "Consommation" in df.columns:
        series = df["Consommation"].copy()
        # Interpolation temporelle + backfill + forward fill
        series = series.interpolate(method='time').bfill().ffill()
        return series
    else:
        return pd.Series(dtype=float)