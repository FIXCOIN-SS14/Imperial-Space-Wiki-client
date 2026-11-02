import webview
import json
import sys
import os
import shutil
import ctypes
import gc
from pathlib import Path

# --- 1. ФЛАГИ ДЛЯ WEBVIEW2 ---
if sys.platform == "win32":
    os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = (
        "--disable-gpu --disable-software-rasterizer "
        "--disable-background-networking --disable-component-update "
        "--disable-sync --disable-translate --no-first-run "
        "--renderer-process-limit=1 "  # Ограничиваем кол-во процессов движка (меньше ОЗУ)
        "--disable-features=CalculateNativeWinOcclusion,HardwareMediaKeyHandling"
    )

CONFIG_FILE = Path.home() / ".imperialspace_wiki.json"
URL = "https://wiki.imperialspace.net"

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
            "width": window.width, "height": window.height, "x": window.x, "y": window.y
        }), "utf-8")
    except Exception:
        pass

def clear_cache() -> None:
    try:
        cache_path = Path(os.getenv("LOCALAPPDATA")) / "imperialspace" / "EBWebView" / "Default" / "Cache"
        if cache_path.exists():
            shutil.rmtree(cache_path, ignore_errors=True)
    except Exception:
        pass

def trim_memory():
    """Принудительно заставляет Windows выгрузить лишнюю ОЗУ из программы"""
    if sys.platform == "win32":
        try:
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.psapi.EmptyWorkingSet(handle)
        except Exception:
            pass
    gc.collect()

def on_loaded(window) -> None:
    """Вызывается при загрузке страницы: убиваем анимации и ставим лимиты"""
    
    # 1. Внедряем CSS, отключающий любую анимацию
    css_js = """
    const style = document.createElement('style');
    style.innerHTML = '*, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }';
    document.head.appendChild(style);
    """
    window.evaluate_js(css_js)

    # 2. Убиваем requestAnimationFrame (самый главный пожиратель FPS)
    # Теперь браузер будет рисовать кадр только при скролле или клике, а не 60 раз в секунду
    raf_js = """
    window.requestAnimationFrame = function() { return 0; };
    window.cancelAnimationFrame = function() { return 0; };
    """
    window.evaluate_js(raf_js)

    # 3. Очищаем ОЗУ
    trim_memory()

def on_closed(window):
    save_config(window)
    clear_cache()

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
    )

    window.events.loaded += on_loaded
    window.events.closed += lambda: on_closed(window)

    webview.start(debug=False)

if __name__ == "__main__":
    main()
