# kalman_model.py
import numpy as np
from filterpy.kalman import KalmanFilter

def init_kalman_filter():
    kf = KalmanFilter(dim_x=2, dim_z=1)
    dt = 1  # time step
    kf.F = np.array([[1, dt],
                     [0, 1]])
    kf.H = np.array([[1, 0]])
    kf.x = np.array([[0], [0]])
    kf.P *= 1000.
    kf.R = 1.
    kf.Q = np.diag([1e-3, 1e-4])
    return kf

def train_kalman_filter(series):
    data = series.values
    kf = init_kalman_filter()
    kf.x = np.array([[data[0]], [0]])
    for z in data:
        kf.predict()
        kf.update([z])
    return kf

def forecast_kalman(kf, steps=96):
    preds = []
    for _ in range(steps):
        kf.predict()
        preds.append(kf.x[0,0])
    return np.array(preds)
