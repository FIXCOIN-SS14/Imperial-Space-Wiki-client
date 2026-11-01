# ImperialSpace Wiki Client

Легкое десктопное приложение-обертка для сайта [wiki.imperialspace.net](https://wiki.imperialspace.net).
Использует системный WebView (не нагружает ОЗУ, в отличие от Electron).

## Как запустить исходный код
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите: `python imperialspace.py`

## Как собрать .exe
`pyinstaller --onefile --windowed --icon=wiki.ico imperialspace.py`