# lstm_model.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def build_lstm_model(n_lags, n_features):
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(n_lags, n_features)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm(series, n_lags=48, epochs=5, batch_size=32):
    # Prepare the series as a numpy array
    values = series.values.astype('float32')
    X, y = [], []
    for i in range(n_lags, len(values)):
        X.append(values[i-n_lags:i])
        y.append(values[i])
    X = np.array(X).reshape(-1, n_lags, 1)
    y = np.array(y)
    model = build_lstm_model(n_lags, n_features=1)
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
    return model

def forecast_lstm(model, recent_history, steps=96, n_lags=48):
    history = list(recent_history.values.astype('float32'))
    forecast = []
    for _ in range(steps):
        input_seq = np.array(history[-n_lags:]).reshape(1, n_lags, 1)
        yhat = model.predict(input_seq, verbose=0)
        forecast.append(yhat[0,0])
        history.append(yhat[0,0])
    return np.array(forecast)
