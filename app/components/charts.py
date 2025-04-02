# charts.py
from dash import html, dcc

def get_chart_area():
    return html.Div(
        children=[
            dcc.Graph(id='forecast-graph'),
            html.Div(id='metrics-div', style={'padding': '10px', 'fontWeight': 'bold'})
        ],
        style={'width': '80%', 'padding': '10px'}
    )
