# server.py
import flask
from dash import Dash
from app import layout  # Import our layout
# Create a Flask server
server = flask.Flask(__name__)

# Create Dash app on top of Flask
app = Dash(__name__, server=server, suppress_callback_exceptions=True)
app.title = "France Electricity Forecasting Dashboard"
app.layout = layout.get_layout()  # Get layout from layout.py

# Import callbacks to register them
from app import callbacks

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
