# app.py

import sys
import webbrowser
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import QTextCodec, QUrl
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWebEngineWidgets import QWebEngineView

from auth_utils import get_auth_url, paste_auth_code, get_access_token, show_confirmation_window
from mainwindow import MainWindow
from mainwindow import AuthWindow


def open_browser_page(url):
    # Открываем браузер с левой стороны экрана
    webbrowser.open(url)

    # Создаем новый виджет для отображения веб-страницы
    view = QWebEngineView()

    # Устанавливаем размеры виджета
    view.setFixedSize(500, 500)

    # Загружаем веб-страницу
    view.load(QUrl(url))

    view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    codec = QTextCodec.codecForName("UTF-8")
    QTextCodec.setCodecForLocale(codec)

    auth_window = AuthWindow()
    main_window = MainWindow()

    auth_window.auth_success.connect(main_window.open_main_window)  # Подключаем сигнал auth_success к методу open_main_window

    auth_window.show()

    app.exec() 