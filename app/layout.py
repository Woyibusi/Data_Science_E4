# layout.py
from dash import html
from app.components import header, sidebar, charts

def get_layout():
    return html.Div([
        header.get_header(),
        html.Div([
            sidebar.get_sidebar(),
            charts.get_chart_area()
        ], style={'display': 'flex'})
    ])
