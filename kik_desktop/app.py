#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from appdirs import *
from kik_unofficial.kikclient import KikClient

from kik_desktop.kik_thread import KikThread
from kik_desktop.ui.login_widget import LoginWidget
from kik_desktop.ui.main_widget import MainWidget, MessageItem, PeerListItem
from kik_desktop.util import load_stylesheet


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = MainWidget()
        self.central_widget = QStackedWidget()
        # sys.excepthook = self.on_exception

        self.partners = {}
        self.messages = {}
        self.peer_list = None
        self.message_list = None
        self.current_peer = None
        self.config = None
        self.kik_thread = None

        self.load_config()
        self.init_ui()

    # def on_exception(self, *args):
    #     print("Exception args: {}".format(*args))
    #     (type, value, traceback) = sys.exc_info()
    #     sys.excepthook(type, value, traceback)

    def init_kik_thread(self):
        self.kik_thread.received_message.connect(self.message_received)
        self.kik_thread.received_group_message.connect(self.group_message_received)
        self.kik_thread.on_login.connect(self.on_login)
        if True:
            self.kik_thread.start()

    def init_ui(self):
        self.setCentralWidget(self.central_widget)
        self.peer_list = self.main_widget.peer_list
        self.message_list = self.main_widget.message_list

        self.main_widget.peer_list.currentItemChanged.connect(self.on_peer_changed)
        self.main_widget.typing_box.returnPressed.connect(self.send_message)

        self.login_widget = LoginWidget(self)
        self.login_widget.login_request.connect(self.login)

        self.central_widget.addWidget(self.login_widget)
        self.central_widget.addWidget(self.main_widget)
        self.setGeometry(0, 0, 920, 640)
        self.setWindowTitle('Kik')
        if 'username' in self.config:
            self.login(self.config['username'], self.config['password'])
        self.show()

    def login(self, username, password):
        print("Attempt login")
        try:
            kik_client = KikClient(username, password)
        except:
            print("Login failed")
            self.login_widget.login_failed()
            return
        self.kik_thread = KikThread(kik_client)
        self.init_kik_thread()
        self.kik_thread.start()
        self.central_widget.setCurrentWidget(self.main_widget)
        self.config['username'] = username
        self.config['password'] = password
        self.save()

    def save(self):
        self.config['messages'] = self.messages
        config_dir = user_config_dir()
        filename = os.path.join(config_dir, 'kik_desktop.json')
        with open(filename, 'w') as file:
            json.dump(self.config, file)

    def load_config(self):
        config_dir = user_config_dir()
        filename = os.path.join(config_dir, 'kik_desktop.json')

        if not os.path.exists(filename):
            print("kik_desktop.json not found at %s" % filename)
            self.config = {'messages': {}}
            return False
        with open(filename, 'r') as file:
            self.config = json.load(file)
            self.messages = self.config['messages']

    def on_peer_changed(self, curr, prev):
        index = self.peer_list.currentIndex().row()
        self.current_peer = list(self.partners.values())[index]
        self.update_message_list()

    def update_message_list(self):
        for i in reversed(range(self.message_list.count())):
            self.message_list.itemAt(i).widget() and self.message_list.itemAt(i).widget().deleteLater()
        if self.current_peer['jid'] not in self.messages:
            return
        messages = self.messages[self.current_peer['jid']]
        for message in messages:
            item = MessageItem(self.get_display_name(message['user']), message['body'])
            self.message_list.addWidget(item)

    def send_message(self):
        sender = self.sender()
        message = sender.text()
        sender.clear()
        self.add_message(self.current_peer['jid'], 'You', message)
        self.update_message_list()
        self.kik_thread.send_message_signal.emit(self.current_peer['jid'], message,
                                                 self.current_peer['type'] == 'group')

    def add_message(self, chat, peer, message):
        if chat not in self.messages:
            self.messages[chat] = []
        self.messages[chat].append({
            'user': peer,
            'body': message
        })
        self.save()

    def message_received(self, peer, message):
        self.add_message(peer, peer, message)
        self.update_message_list()

    def group_message_received(self, chat, peer, message):
        self.add_message(chat, peer, message)
        self.update_message_list()

    def on_login(self):
        print("On login")
        partners = self.kik_thread.partners
        self.partners = OrderedDict(partners)
        sorted_keys = sorted(self.partners, key=lambda e: self.full_name(self.partners[e]))
        [self.partners.move_to_end(key) for key in sorted_keys]
        for jid in self.partners:
            partner = self.partners[jid]
            item = PeerListItem()
            item.set_title_label(self.full_name(partner))
            if 'picture_url' in partner and partner['picture_url'] is not None:
                item.set_icon(partner['picture_url'] + "/thumb.jpg")
            self.main_widget.add_item(item)
        if self.peer_list.count() > 0:
            self.peer_list.setCurrentRow(0)

    def get_name(self, jid):
        if jid in self.partners.keys():
            return self.full_name(self.partners[jid])
        return jid

    def get_display_name(self, jid):
        if jid in self.partners.keys():
            return self.partners[jid]['display_name']
        return jid

    @staticmethod
    def full_name(peer):
        if peer['type'] == 'group':
            if peer['public']:
                return "{} ({})".format(peer['display_name'], peer['code'])
            else:
                if peer['display_name']:
                    return "{}".format(peer['display_name'])
                else:
                    return "Group: " + ", ".join([App.jid_to_username(member['jid']) for member in peer['users']])
        else:
            return "{} ({})".format(peer['display_name'], peer['username'])

    @staticmethod
    def jid_to_username(jid):
        return str(jid.split("@")[0][0:-4])

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


def execute():
    app = QApplication(sys.argv)
    ex = App()
    ex.setStyleSheet(load_stylesheet('light_theme.css'))
    sys.exit(app.exec_())


if __name__ == '__main__':
    execute()
