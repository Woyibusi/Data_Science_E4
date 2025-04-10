# preprocess.py
import pandas as pd

def clean_series(df):
    # Assume the column "Consommation" contains the consumption data.
    if "Consommation" in df.columns:
        series = df["Consommation"].copy()
        # Fill missing values using time interpolation
        series = series.interpolate(method='time')
        series = series.ffill()

        return series
    else:
        return pd.Series()
