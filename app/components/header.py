# header.py
from dash import html

def get_header():
    return html.Div(
        children=[
            html.H1("France Electricity Forecasting Dashboard", style={'textAlign': 'center'})
        ],
        style={'backgroundColor': '#f8f9fa', 'padding': '10px'}
    )
