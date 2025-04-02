import threading
import webbrowser
from app.server import app

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

if __name__ == "__main__":
    # Start a timer to open the browser after a short delay
    threading.Timer(1, open_browser).start()
    # Bind the app to 127.0.0.1 instead of 0.0.0.0
    app.run_server(debug=True, host='127.0.0.1', port=8050)
