import hashlib
import os
import sys
import urllib.request

from PyQt5.QtCore import Qt, QThread, QPointF
from PyQt5.QtGui import QPixmap, QBrush, QPainter
from PyQt5.QtWidgets import QWidget, QListWidget, QHBoxLayout, QSplitter, QLineEdit, QVBoxLayout, \
    QLabel, QScrollArea, QLayout, QApplication, QListWidgetItem
from appdirs import user_cache_dir

from kik_desktop.util import load_stylesheet


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.typing_box = QLineEdit()
        self.peer_list = QListWidget()
        self.message_list = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        main_box = QHBoxLayout()
        hsplitter = QSplitter(Qt.Horizontal)

        self.init_peer_list()
        hsplitter.addWidget(self.peer_list)

        message_box = self.create_message_box()
        hsplitter.addWidget(message_box)
        hsplitter.setChildrenCollapsible(False)
        hsplitter.setSizes([1000, 3000])

        main_box.addWidget(hsplitter, 1)
        main_box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_box)

    def init_peer_list(self):
        pass
        self.peer_list.setObjectName("peerList")
        self.peer_list.setMinimumSize(300, 400)
        self.peer_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def create_message_box(self):
        container = QWidget()
        container.setObjectName("messageContainer")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        container.setLayout(layout)

        typingContainer = QWidget()
        typingContainer.setObjectName("typingContainer")
        typingLayout = QHBoxLayout()
        typingContainer.setLayout(typingLayout)
        typingLayout.addWidget(self.typing_box)
        self.typing_box.setPlaceholderText("Write a message...")
        self.typing_box.setObjectName("typingBox")

        self.message_list.setObjectName("messageBox")
        self.message_list.setSpacing(0)
        self.message_list.setContentsMargins(0, 0, 0, 0)

        self.message_scroll_area = QScrollArea()
        bar = self.message_scroll_area.verticalScrollBar()
        bar.rangeChanged.connect(self.range_changed)
        self.message_scroll_area.setWidgetResizable(True)
        client = QWidget()
        client.setMaximumWidth(800)
        self.message_scroll_area.setWidget(client)
        self.message_scroll_area.setAlignment(Qt.AlignCenter)
        client.setLayout(self.message_list)

        self.message_list.addStretch()

        layout.addWidget(self.message_scroll_area, stretch=1)
        layout.addWidget(typingContainer, stretch=0, alignment=Qt.AlignBottom)

        return container

    def range_changed(self, min, max):
        self.message_scroll_area.verticalScrollBar().setValue(max)

    def add_item(self, item):
        widget_item = QListWidgetItem(self.peer_list)
        widget_item.setSizeHint(item.sizeHint())
        self.peer_list.addItem(widget_item)
        self.peer_list.setItemWidget(widget_item, item)


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
        name_label = QLabel('<b>' + self.user + ':</b>')
        name_label.setObjectName("nameLabel")
        text_label = QLabel(self.message)
        text_label.setObjectName("textLabel")
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(name_label, alignment=Qt.AlignLeft)
        layout.addWidget(text_label, alignment=Qt.AlignLeft)

        client = QWidget()
        client.setObjectName("ownMessage" if self.user == "You" else "message")
        client.setLayout(layout)
        if self.user == "You":
            box_layout.addWidget(client, alignment=Qt.AlignRight)
        else:
            box_layout.addWidget(client, alignment=Qt.AlignLeft)

        box_layout.setSpacing(0)
        box_layout.setContentsMargins(10, 3, 2, 3)

        self.setLayout(box_layout)


class PeerListItem(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.icon = RoundedCornerImage()
        self.title_label = QLabel()
        self.last_message_label = QLabel()
        self.time_label = QLabel()
        self.unread_message_label = QLabel()
        self.init_ui()

    def set_icon(self, url):
        self.icon_download_thread = OnlinePixmapThread(url)
        self.icon_download_thread.finished.connect(self.on_icon_retrieved)
        self.icon_download_thread.start()

    def on_icon_retrieved(self):
        scaled = self.scale_image(self.icon_download_thread.pixmap)
        self.icon.setPixmap(scaled)
        self.icon.setFixedSize(48, 48)

    @staticmethod
    def scale_image(pixmap):
        scaled = pixmap.scaled(48, 48, transformMode=Qt.SmoothTransformation)
        return scaled

    def set_title_label(self, text):
        self.title_label.setText(text)

    def set_last_message_label(self, text):
        self.last_message_label.setText(text)

    def set_time_label(self, text):
        self.time_label.setText(text)

    def set_unread_message_label(self, text):
        self.unread_message_label.setText(text)

    def init_ui(self):
        self.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.icon.setFixedSize(48, 48)
        self.layout.addWidget(self.icon, alignment=Qt.AlignLeft)

        middle_box = QVBoxLayout()
        middle_box.addWidget(self.title_label, alignment=Qt.AlignLeft)
        middle_box.addWidget(self.last_message_label, alignment=Qt.AlignLeft)
        middle_box.setContentsMargins(0, 0, 0, 0)
        middle_box.setSpacing(0)

        self.layout.addLayout(middle_box)
        self.layout.addStretch()

        end_box = QVBoxLayout()
        end_box.addWidget(self.time_label, alignment=Qt.AlignRight)
        end_box.addWidget(self.unread_message_label, alignment=Qt.AlignRight)
        end_box.setContentsMargins(0, 0, 0, 0)
        end_box.setSpacing(0)

        self.layout.addLayout(end_box)


class RoundedCornerImage(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFixedSize(48, 48)

    def paintEvent(self, QPaintEvent):
        pixmap = self.pixmap()
        if pixmap:
            brush = QBrush(pixmap)
            painter = QPainter()
            painter.begin(self)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.fillRect(0, 0, 48, 48, Qt.transparent)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawEllipse(QPointF(24, 24), 23, 23)
            painter.end()


class OnlinePixmapThread(QThread):
    def __init__(self, url):
        QThread.__init__(self)
        self.url = url
        self.pixmap = None

    def __del__(self):
        self.wait()

    def run(self):
        cache_dir = user_cache_dir('kik_desktop')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        path = cache_dir + "/" + hashlib.md5(self.url.encode('utf-8')).hexdigest() + ".jpg"
        if os.path.exists(path):
            self.pixmap = QPixmap(path)
            return
        print("Downloading {} to {}".format(self.url, path))
        urllib.request.urlretrieve(self.url, path)
        self.pixmap = QPixmap(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.setStyleSheet(load_stylesheet('../light_theme.css'))
    ex.show()
    for i in range(80):
        ex.message_list.addWidget(MessageItem("You", "hi"))
        ex.message_list.addWidget(MessageItem("Someone", "hey"))

    ex.message_list.addWidget(MessageItem("You", "what's up?"))
    ex.message_list.addWidget(MessageItem("Someone", "Nothing."))
    for i in range(4):
        item = PeerListItem()
        item.set_icon("/home/jaap/aXm3017xjU.jpg")
        item.set_title_label("TI Menschen")
        item.set_last_message_label("<b>Jean:</b> Hi")
        ex.add_item(item)

    sys.exit(app.exec_())
