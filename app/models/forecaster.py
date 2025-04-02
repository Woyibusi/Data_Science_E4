# forecaster.py
def forecast(model_name, train_series, test_steps):
    if model_name.lower() == 'sarimax':
        from .arima_model import train_sarimax, forecast_sarimax
        model = train_sarimax(train_series)
        return forecast_sarimax(model, steps=test_steps)
    elif model_name.lower() == 'lstm':
        from .lstm_model import train_lstm, forecast_lstm
        model = train_lstm(train_series)
        return forecast_lstm(model, train_series[-48:], steps=test_steps)
    elif model_name.lower() == 'kalman':
        from .kalman_model import train_kalman_filter, forecast_kalman
        model = train_kalman_filter(train_series)
        return forecast_kalman(model, steps=test_steps)
    else:
        raise ValueError("Unknown model")
