# callbacks.py
from dash import Input, Output
import requests
import plotly.graph_objs as go
import pandas as pd
from app import data  # to access our data loader module
from app.data import data_loader, preprocess
from app.server import app

@app.callback(
    Output('forecast-graph', 'figure'),
    Output('metrics-div', 'children'),
    Input('model-dropdown', 'value'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_forecast(selected_model, start_date, end_date):
    # Load full data from CSVs located in app/data/
    df = data_loader.load_consumption_data("app/data")
    series = preprocess.clean_series(df)
    
    if start_date and end_date:
        series = series.loc[start_date:end_date]
    
    # Simple split: 80% train, 20% test
    split_idx = int(0.8 * len(series))
    train_series = series.iloc[:split_idx]
    test_series = series.iloc[split_idx:]
    
    # Call backend API to get forecast
    try:
        response = requests.get("http://localhost:8000/forecast", params={
            "model": selected_model,
            "start": start_date,
            "end": end_date
        })
        result = response.json()
        forecast = result.get("forecast", [])
        model_name = result.get("model_name", selected_model)
        metrics = result.get("metrics", {})
    except Exception as e:
        forecast = []
        model_name = selected_model
        metrics = {"error": str(e)}
    
    # Create Plotly figure: actual data and forecast overlay
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode='lines', name='Actual'))
    if forecast:
        # Assume forecast covers test_series dates
        forecast_index = test_series.index
        fig.add_trace(go.Scatter(x=forecast_index, y=forecast, mode='lines', name=f'{model_name} Forecast'))
    
    metrics_text = ""
    if metrics:
        metrics_text = " | ".join([f"{k}: {v:.2f}" if isinstance(v, (float, int)) else f"{k}: {v}" for k, v in metrics.items()])
    
    return fig, metrics_text
