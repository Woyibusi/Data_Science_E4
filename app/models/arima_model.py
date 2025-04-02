# arima_model.py
from statsmodels.tsa.statespace.sarimax import SARIMAX

def train_sarimax(series, exog_train=None):
    # Example orders – adjust as needed.
    model = SARIMAX(series, order=(1,1,1), seasonal_order=(1,0,1,96), exog=exog_train)
    results = model.fit(disp=False)
    return results

def forecast_sarimax(fitted_model, steps, exog_future=None):
    forecast_obj = fitted_model.get_forecast(steps=steps, exog=exog_future)
    return forecast_obj.predicted_mean.values
