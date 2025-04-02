# sidebar.py
from dash import html, dcc
import datetime

def get_sidebar():
    return html.Div(
        children=[
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-range-picker',
                min_date_allowed=datetime.date(2023, 1, 1),
                max_date_allowed=datetime.date(2025, 12, 31),
                start_date=datetime.date(2024, 1, 1),
                end_date=datetime.date(2024, 12, 31)
            ),
            html.Br(),
            html.Label("Select Forecast Model:"),
            dcc.Dropdown(
                id='model-dropdown',
                options=[
                    {'label': 'SARIMAX', 'value': 'sarimax'},
                    {'label': 'LSTM', 'value': 'lstm'},
                    {'label': 'Kalman Filter', 'value': 'kalman'}
                ],
                value='sarimax'
            )
        ],
        style={'width': '20%', 'padding': '10px', 'backgroundColor': '#e9ecef'}
    )
