import webview
import json
import sys
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".imperialspace_wiki.json"
URL = "https://wiki.imperialspace.net"

# Эта функция нужна, чтобы .exe находил иконку внутри себя
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import webview
import json
import sys
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".imperialspace_wiki.json"
URL = "https://wiki.imperialspace.net"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"width": 1280, "height": 820, "x": None, "y": None}

def save_config(window) -> None:
    try:
        CONFIG_FILE.write_text(json.dumps({
            "width": window.width,
            "height": window.height,
            "x": window.x,
            "y": window.y,
        }), "utf-8")
    except Exception:
        pass

def main() -> None:
    cfg = load_config()

    window = webview.create_window(
        title="ImperialSpace Wiki",
        url=URL,
        width=cfg["width"],
        height=cfg["height"],
        x=cfg["x"],
        y=cfg["y"],
        min_size=(700, 500),
        text_select=True,
        confirm_close=False
        # window_icon=...  <-- ЭТУ СТРОКУ НУЖНО УБРАТЬ
    )

    window.events.closed += lambda: save_config(window)
    webview.start(debug=False)

if __name__ == "__main__":
    main()