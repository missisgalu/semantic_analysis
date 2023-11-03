# auth_utils.py

from urllib.parse import urlencode
from PyQt5.QtWidgets import QApplication, QMessageBox

from modules.cl import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET

import requests

def get_auth_url():
    try:
        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code"
        }

        auth_url = f"https://hh.ru/oauth/authorize?{urlencode(params)}"

        return auth_url
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при получении URL авторизации: {str(e)}")
        return None

def paste_auth_code():
    try:
        auth_code = QApplication.clipboard().text()
        if auth_code:
            return auth_code
        else:
            QMessageBox.critical(None, "Ошибка", "Буфер обмена пуст. Скопируйте код авторизации и попробуйте снова.")
            return None
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при получении кода авторизации: {str(e)}")
        return None

def show_confirmation_window():
    try:
        confirmation_window = QMessageBox()
        confirmation_window.setWindowTitle("Успешная авторизация")
        confirmation_window.setText("Авторизация прошла успешно!")
        confirmation_window.addButton(QMessageBox.Close)
        confirmation_window.show()
        confirmation_window.exec()
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при отображении окна подтверждения: {str(e)}")

def get_access_token(code):
    try:
        data = {
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code
        }

        token_url = "https://hh.ru/oauth/token"

        response = requests.post(token_url, data=data)

        if response.status_code != 200:
            raise Exception("Ошибка авторизации: Введите корректный код авторизации")

        access_token = response.json().get("access_token")

        return access_token
    except Exception as e:
        raise Exception("Ошибка при получении токена доступа: " + str(e))