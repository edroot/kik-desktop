import re
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QApplication, QVBoxLayout, \
    QDateEdit, QHBoxLayout
from kik_unofficial.kik_exceptions import KikCaptchaException
from kik_unofficial.kikclient import KikClient, KikErrorException

from kik_desktop.util import load_stylesheet


class RegisterWidget(QWidget):
    login_request = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(RegisterWidget, self).__init__(parent)
        self.kik_client = KikClient()
        self.interceptor = RequestInterceptor(self)
        self.error_label = QLabel()
        self.webview = QWebEngineView()
        self.login_button = QPushButton()
        self.birthday_edit = QDateEdit()
        self.password_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.init_ui()

    def init_ui(self):
        main_box = QVBoxLayout()
        main_box.setSpacing(20)
        main_box.setAlignment(Qt.AlignCenter)

        label = QLabel("Sign up")
        main_box.addWidget(label, alignment=Qt.AlignCenter)

        self.first_name_edit.setPlaceholderText("First name")
        main_box.addWidget(self.first_name_edit, alignment=Qt.AlignCenter)

        self.last_name_edit.setPlaceholderText("Last name")
        main_box.addWidget(self.last_name_edit, alignment=Qt.AlignCenter)

        self.username_edit.setPlaceholderText("Username")
        main_box.addWidget(self.username_edit, alignment=Qt.AlignCenter)

        self.email_edit.setPlaceholderText("Email")
        main_box.addWidget(self.email_edit, alignment=Qt.AlignCenter)

        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Password")
        main_box.addWidget(self.password_edit, alignment=Qt.AlignCenter)

        self.birthday_edit.setCalendarPopup(True)
        self.birthday_edit.setDisplayFormat("yyyy-MM-dd")

        birthday_layout = QHBoxLayout()
        birthday_label = QLabel("Birthday:")
        birthday_layout.addWidget(birthday_label, alignment=Qt.AlignCenter)
        birthday_layout.addWidget(self.birthday_edit, alignment=Qt.AlignCenter)
        birthday_layout.setAlignment(Qt.AlignCenter)
        main_box.addLayout(birthday_layout)

        self.login_button.setText("Sign up")
        self.login_button.clicked.connect(self.sign_up)
        main_box.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.error_label.setObjectName("errorLabel")
        main_box.addWidget(self.error_label, alignment=Qt.AlignCenter)

        main_box.addWidget(self.webview, alignment=Qt.AlignCenter)

        self.setLayout(main_box)
        self.show()

    def sign_up(self):
        self.error_label.setText("")
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        birthday = self.birthday_edit.date()
        try:
            self.kik_client.sign_up(email, username, password, first_name, last_name,
                                          birthday.toString("yyyy-MM-dd"))
        except KikCaptchaException as e:
            url = e.captcha_url + "&callback_url=https://kik.com/captcha-url"
            self.webview.load(QUrl(url))
            self.webview.page().profile().setHttpUserAgent(
                "Mozilla/5.0 (Linux; Android 7.1.2; Nexus 7 Build/NJH47F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.78 Safari/537.36")
            self.webview.page().profile().setRequestInterceptor(self.interceptor)
        except Exception as e:
            self.error_label.setText(str(e))
            return False

    def on_captcha_response(self, captcha_result):
        print("Received response: {}".format(captcha_result))
        self.sign_up_captcha(captcha_result)

    def sign_up_captcha(self, captcha_result):
        self.error_label.setText("")
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        username = self.username_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        birthday = self.birthday_edit.date()
        try:
            node = self.kik_client.sign_up(email, username, password, first_name, last_name,
                                           birthday.toString("yyyy-MM-dd"), captcha_result)
            print(node)
            self.login_request.emit(username, password)
        except:
            self.error_label.setText("Account creation failed")


class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info: QWebEngineUrlRequestInfo):
        url = info.requestUrl().toString()  # type: QUrl
        match = re.match("https?://kik.com/captcha-url\?response=(.*)", url)
        if match:
            print("Captcha response found")
            print(match.group(1))
            self.parent().on_captcha_response(match.group(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterWidget()
    ex.setStyleSheet(load_stylesheet('light_theme.css'))
    ex.show()
    sys.exit(app.exec_())
