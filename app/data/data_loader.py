# data_loader.py
import pandas as pd
import os

def load_consumption_data(data_dir):
    # List your energy CSV files
    file_names = ["energy_data2023.csv", "energy_data2024.csv", "energy_data2025.csv"]
    dfs = []
    for file in file_names:
        file_path = os.path.join(data_dir, file)
        try:
            df = pd.read_csv(file_path, sep=";", parse_dates=["datetime"], dayfirst=True)
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    if dfs:
        combined = pd.concat(dfs).sort_values("datetime")
        combined.set_index("datetime", inplace=True)
        return combined
    else:
        return pd.DataFrame()
