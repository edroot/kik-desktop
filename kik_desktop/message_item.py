from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLayout, QHBoxLayout


class MessageItem(QWidget):
    def __init__(self, user, message):
        super().__init__()
        self.user = user
        self.message = message
        self.init_ui()

    def init_ui(self):
        box_layout = QHBoxLayout()
        layout = QHBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        name_label = QLabel('<b>' + (self.user if self.user else "You") + ':</b>')
        name_label.setObjectName("nameLabel")
        text_label = QLabel(self.message)
        text_label.setObjectName("textLabel")
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(name_label, alignment=Qt.AlignLeft)
        layout.addWidget(text_label, alignment=Qt.AlignLeft)

        client = QWidget()
        client.setObjectName("ownMessage" if not self.user else "message")
        client.setLayout(layout)
        if not self.user:
            box_layout.addWidget(client, alignment=Qt.AlignRight)
        else:
            box_layout.addWidget(client, alignment=Qt.AlignLeft)

        box_layout.setSpacing(0)
        box_layout.setContentsMargins(0, 2, 0, 8)

        self.setLayout(box_layout)
