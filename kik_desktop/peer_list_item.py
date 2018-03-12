import hashlib
import os
import urllib

from PyQt5.QtCore import Qt, QPointF, QThread
from PyQt5.QtGui import QBrush, QPainter, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from appdirs import user_cache_dir


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
        cache_dir = user_cache_dir('kik_desktop_legacy')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        path = cache_dir + "/" + hashlib.md5(self.url.encode('utf-8')).hexdigest() + ".jpg"
        if os.path.exists(path):
            self.pixmap = QPixmap(path)
            return
        print("Downloading {} to {}".format(self.url, path))
        urllib.request.urlretrieve(self.url, path)
        self.pixmap = QPixmap(path)
