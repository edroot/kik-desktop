# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layouts/login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(1024, 640)
        font = QtGui.QFont()
        font.setPointSize(12)
        LoginWindow.setFont(font)
        LoginWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(54, 54, 54);")
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(11)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(122, 122, 122);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.username_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.username_edit.setMinimumSize(QtCore.QSize(400, 0))
        self.username_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.username_edit.setObjectName("username_edit")
        self.verticalLayout.addWidget(self.username_edit, 0, QtCore.Qt.AlignHCenter)
        self.password_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_edit.setMinimumSize(QtCore.QSize(400, 0))
        self.password_edit.setMaximumSize(QtCore.QSize(400, 16777215))
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setObjectName("password_edit")
        self.verticalLayout.addWidget(self.password_edit, 0, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(400, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(89, 200, 23);\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.error_text = QtWidgets.QLabel(self.centralwidget)
        self.error_text.setEnabled(True)
        self.error_text.setStyleSheet("font-weight: bold;\n"
"color: #F00;\n"
"font-size: 18px;")
        self.error_text.setText("")
        self.error_text.setObjectName("error_text")
        self.verticalLayout.addWidget(self.error_text, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoginWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 19))
        self.menubar.setObjectName("menubar")
        LoginWindow.setMenuBar(self.menubar)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Kik Unofficial - Login"))
        self.label.setText(_translate("LoginWindow", "Log in"))
        self.username_edit.setPlaceholderText(_translate("LoginWindow", "Username"))
        self.password_edit.setPlaceholderText(_translate("LoginWindow", "Password"))
        self.pushButton.setText(_translate("LoginWindow", "Login"))

