# model_trainer.py
def train_all_models(data):
    from .arima_model import train_sarimax
    from .lstm_model import train_lstm
    from .kalman_model import train_kalman_filter
    model_sarimax = train_sarimax(data)
    model_lstm = train_lstm(data)
    model_kalman = train_kalman_filter(data)
    return {
        'sarimax': model_sarimax,
        'lstm': model_lstm,
        'kalman': model_kalman
    }
