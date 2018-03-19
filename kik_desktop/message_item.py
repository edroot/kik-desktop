from PyQt5.QtCore import QDateTime, QDate
from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy

from kik_desktop.ui import message_item_layout


class MessageItem(QWidget):
    def __init__(self, user, message, timestamp, show_name=True):
        super().__init__()
        self.ui = message_item_layout.Ui_message()
        self.ui.setupUi(self)
        self.ui.username.setText(user if user else "You")
        self.ui.myFrame.setObjectName("myFrame" if not user else "theirFrame")
        if not user or not show_name:
            self.ui.username.deleteLater()
        self.ui.body.setText(message)
        self.ui.time.setText(format_date(QDateTime.fromSecsSinceEpoch(int(timestamp))))
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.ui.horizontalLayout.insertSpacerItem(1 if user else 0, spacer)
        self.ui.horizontalLayout.setStretch(1 if user else 0, 1)

    # def init_ui(self):
    # self.setContentsMargins(0, 0, 0, 0)
    # row_layout = QHBoxLayout()
    # message_layout = QHBoxLayout()
    # message_layout.setSizeConstraint(QLayout.SetFixedSize)
    #
    # client = QWidget()
    # client.setObjectName("ownMessage" if not self.user else "message")
    # client.setLayout(message_layout)
    #
    # name_label = QLabel('<b>' + (self.user if self.user else "You") + ':</b>')
    # name_label.setObjectName("nameLabel")
    # text_label = QLabel(self.message)
    # text_label.setObjectName("textLabel")
    # text_label.setWordWrap(True)
    # text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    # message_layout.addWidget(name_label, alignment=Qt.AlignLeft)
    # message_layout.addWidget(text_label, alignment=Qt.AlignLeft)
    #
    # if not self.user:
    #     # layout.setContentsMargins(10, 2, 30, 5)
    #     row_layout.addWidget(client, alignment=Qt.AlignRight)
    # else:
    #     row_layout.addWidget(client, alignment=Qt.AlignLeft)
    #     # layout.setContentsMargins(30, 2, 10, 5)
    #
    # row_layout.setSpacing(0)
    # row_layout.setContentsMargins(0, 0, 0, 0)
    # message_layout.setSpacing(0)
    # message_layout.setContentsMargins(0, 0, 0, 0)
    #
    # self.setLayout(row_layout)


def format_date(date: QDateTime):
    if date.date() == QDate.currentDate():
        return date.time().toString("hh:mm")
    else:
        return date.toString("ddd, MMMM d hh:mm ap")
