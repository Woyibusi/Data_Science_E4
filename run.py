import threading
import webbrowser
from app.server import app

def open_browser():
    # Open the browser on localhost; note that this auto-open may not work reliably inside a Docker container.
    webbrowser.open_new("http://127.0.0.1:8050")

if __name__ == "__main__":
    # When running locally, this will open a browser window.
    threading.Timer(1, open_browser).start()
    # In Docker, binding to 0.0.0.0 ensures external accessibility.
    app.run(debug=True, host='0.0.0.0', port=8050)
