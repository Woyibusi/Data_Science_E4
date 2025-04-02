from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.data import data_loader, preprocess
from app.models import arima_model, lstm_model, kalman_model

backend_app = FastAPI()

# Load data once at startup
full_data = data_loader.load_consumption_data("app/data")
full_data = preprocess.clean_series(full_data)

@backend_app.get("/forecast")
def get_forecast(model: str, start: str = None, end: str = None):
    # 1) Filter data by dates
    series = full_data
    if start:
        series = series[series.index >= pd.to_datetime(start)]
    if end:
        series = series[series.index <= pd.to_datetime(end)]
    
    # 2) Split data into train/test
    split_idx = int(0.8 * len(series))
    train_series = series.iloc[:split_idx]
    test_series = series.iloc[split_idx:]
    
    # 3) Train & forecast
    if model.lower() == "sarimax":
        fitted = arima_model.train_sarimax(train_series)
        y_pred = arima_model.forecast_sarimax(fitted, steps=len(test_series))
        model_name = "SARIMAX"
    elif model.lower() == "lstm":
        lstm = lstm_model.train_lstm(train_series)
        y_pred = lstm_model.forecast_lstm(lstm, train_series[-48:], steps=len(test_series))
        model_name = "LSTM"
    elif model.lower() == "kalman":
        kf = kalman_model.train_kalman_filter(train_series)
        y_pred = kalman_model.forecast_kalman(kf, steps=len(test_series))
        model_name = "Kalman Filter"
    else:
        return {"error": f"Unknown model: {model}"}
    
    # 4) Compute metrics
    y_true = test_series.values
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mape = float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)

    return {
        "model_name": model_name,
        "forecast": list(y_pred),
        "metrics": {
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape
        }
    }
