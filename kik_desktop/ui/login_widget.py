import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QApplication


class LoginWidget(QWidget):
    login_request = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.login_button = QPushButton()
        self.error_label = QLabel()
        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.setStyleSheet("""
QLabel {
font: 20px;
color: #333;
}
QLabel#errorLabel {
color: red;
}
QLineEdit {
background-color: white;
border: 1px solid #DDD;
padding: 5px 10px;
width: 300px;
color: #333;
font: bold 16px;
border-radius: 0px;
}
QPushButton {
background-color: #59c817;
border: none;
color: white;
font: 18px;
padding: 12px 20px;
}
        """)
        self.init_ui()

    def init_ui(self):
        main_box = QVBoxLayout()
        main_box.setSpacing(20)
        main_box.setAlignment(Qt.AlignCenter)

        label = QLabel("Log in to Kik")

        self.username_field.setPlaceholderText("Email or Kik Username")
        self.username_field.returnPressed.connect(self.username_field_return_pressed)

        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.returnPressed.connect(self.password_field_return_pressed)

        self.login_button.setText("Sign in")
        self.login_button.clicked.connect(self.login_button_clicked)

        self.error_label.setObjectName("errorLabel")

        main_box.addWidget(label, alignment=Qt.AlignCenter)
        main_box.addWidget(self.username_field, alignment=Qt.AlignCenter)
        main_box.addWidget(self.password_field, alignment=Qt.AlignCenter)
        main_box.addWidget(self.login_button, alignment=Qt.AlignCenter)
        main_box.addWidget(self.error_label, alignment=Qt.AlignCenter)

        self.setLayout(main_box)
        self.show()

    def username_field_return_pressed(self):
        self.password_field.setFocus()

    def password_field_return_pressed(self):
        self.login()

    def login_button_clicked(self):
        self.login()

    def login(self):
        self.error_label.setText("")
        if self.check_form():
            self.login_button.setText("Signing in...")
            self.login_button.setEnabled(False)
            self.username_field.setEnabled(False)
            self.password_field.setEnabled(False)
            self.login_request.emit(self.username_field.text(), self.password_field.text())

    def check_form(self):
        if not self.username_field.text():
            self.set_error("Username required")
            self.username_field.selectAll()
            self.username_field.setFocus()
            return False
        if not self.password_field.text():
            self.set_error("Password required")
            self.password_field.selectAll()
            self.password_field.setFocus()
            return False
        if len(self.password_field.text()) < 6:
            self.set_error("Password too short")
            self.password_field.selectAll()
            self.password_field.setFocus()
            return False
        return True

    def set_error(self, error):
        self.error_label.setText(error)

    def login_failed(self):
        self.error_label.setText("Could not log in")
        self.login_button.setText("Sign in")
        self.login_button.setEnabled(True)
        self.username_field.setEnabled(True)
        self.password_field.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWidget()
    ex.show()
    sys.exit(app.exec_())
