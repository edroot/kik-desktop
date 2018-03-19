# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layouts/message_item_layout.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_message(object):
    def setupUi(self, message):
        message.setObjectName("message")
        message.resize(224, 132)
        message.setStyleSheet("#message {\n"
"}\n"
"\n"
"QFrame {\n"
"border-radius: 5px;\n"
"padding: 2px;\n"
"}\n"
"QLabel {\n"
"margin-top: -4px;\n"
"margin-bottom: -4px;\n"
"}\n"
"\n"
"#myFrame {\n"
"background-color: #5dcd11;\n"
"}\n"
"\n"
"#theirFrame {\n"
"background-color: #ffffff;\n"
"}\n"
"\n"
"#username {\n"
"font-weight: bold;\n"
"color: #5dcd11;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#body {\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#time {\n"
"color: #999;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"#myFrame #time {\n"
"    color: #ddd;\n"
"}\n"
"#myFrame #body {\n"
"    color: white;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(message)
        self.horizontalLayout.setContentsMargins(12, 2, 12, 2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.myFrame = QtWidgets.QFrame(message)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myFrame.sizePolicy().hasHeightForWidth())
        self.myFrame.setSizePolicy(sizePolicy)
        self.myFrame.setMinimumSize(QtCore.QSize(200, 0))
        self.myFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.myFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.myFrame.setObjectName("myFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.myFrame)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.username = QtWidgets.QLabel(self.myFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username.sizePolicy().hasHeightForWidth())
        self.username.setSizePolicy(sizePolicy)
        self.username.setStyleSheet("")
        self.username.setObjectName("username")
        self.verticalLayout_2.addWidget(self.username)
        self.body = QtWidgets.QLabel(self.myFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy)
        self.body.setMaximumSize(QtCore.QSize(261, 16777215))
        self.body.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.body.setWordWrap(True)
        self.body.setObjectName("body")
        self.verticalLayout_2.addWidget(self.body)
        self.time = QtWidgets.QLabel(self.myFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.time.sizePolicy().hasHeightForWidth())
        self.time.setSizePolicy(sizePolicy)
        self.time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time.setObjectName("time")
        self.verticalLayout_2.addWidget(self.time)
        self.horizontalLayout.addWidget(self.myFrame)

        self.retranslateUi(message)
        QtCore.QMetaObject.connectSlotsByName(message)

    def retranslateUi(self, message):
        _translate = QtCore.QCoreApplication.translate
        message.setWindowTitle(_translate("message", "Form"))
        self.username.setText(_translate("message", "Username"))
        self.body.setText(_translate("message", "sodlkfj sdofij sdf oskdjf osdkjf okasdjf lksdjf lskdjkfl sjd "))
        self.time.setText(_translate("message", "Time"))

