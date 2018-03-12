import json
import logging
import os
import sys
import time
from typing import List

import appdirs
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.errors import SignUpError, LoginError
from kik_unofficial.datatypes.peers import Peer, Group, User
from kik_unofficial.datatypes.xmpp.chatting import IncomingStatusResponse, IncomingGroupReceiptsEvent, IncomingGroupStatus, IncomingIsTypingEvent, \
    IncomingChatMessage, IncomingGroupIsTypingEvent, IncomingMessageDeliveredEvent, IncomingMessageReadEvent, IncomingFriendAttribution, \
    IncomingGroupChatMessage
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeerInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import ConnectionFailedResponse, RegisterResponse, UsernameUniquenessResponse, LoginResponse

from kik_desktop.message_item import MessageItem
from kik_desktop.peer_list_item import PeerListItem
from kik_desktop.ui import login_ui, main_ui

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('kik_desktop')

config_file = appdirs.user_config_dir() + '/kik_desktop.json'
config = {
    'messages': {}
}


class App(QMainWindow):
    on_authorized_signal = pyqtSignal()
    peers_updated_signal = pyqtSignal()
    messages_updated_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        global kik_client
        self.main_ui = main_ui.Ui_MainWindow()
        self.login_ui = login_ui.Ui_LoginWindow()
        if 'username' in config and 'password' in config:
            self.main_ui.setupUi(self)
            if 'node' in config:
                kik_client = KikClient(KikCallback(), config['username'], config['password'], config['node'], log_level=logging.DEBUG)
            else:
                kik_client = KikClient(KikCallback(), config['username'], config['password'], log_level=logging.DEBUG)
        else:
            kik_client = KikClient(KikCallback(), log_level=logging.DEBUG)
            self.login_ui.setupUi(self)
            self.login_ui.pushButton.clicked.connect(self.login)

        self.on_authorized_signal.connect(self.on_authorized)
        self.peers_updated_signal.connect(self.peers_updated)
        self.messages_updated_signal.connect(self.messages_updated)
        self.current_peer = None
        self.peers = []
        self.jid_peers = {}

    def messages_updated(self, jid):
        if jid == self.current_peer.jid:
            message = config['messages'][jid][-1]
            self.add_message(message)
            self.main_ui.messages.scrollToBottom()

    @pyqtSlot()
    def on_authorized(self):
        self.setup_main_ui()
        kik_client.request_roster()

    def setup_main_ui(self):
        self.main_ui.setupUi(self)
        self.main_ui.messageEdit.returnPressed.connect(self.send)
        self.main_ui.users.currentItemChanged.connect(self.change_current_peer)

    def change_current_peer(self, old, new):
        index = self.main_ui.users.currentIndex().row()
        self.current_peer = self.peers[index]
        self.main_ui.userLabel.setText(self.display_name(self.current_peer))
        self.main_ui.messages.clear()
        if self.current_peer.jid in config['messages']:
            messages = config['messages'][self.current_peer.jid]
            for message in messages:
                self.add_message(message)
            self.main_ui.messages.scrollToBottom()

    def add_message(self, message):
        item = MessageItem(self.display_name_jid(message['jid']) if 'jid' in message else None, message['body'])
        widget_item = QListWidgetItem(self.main_ui.messages)
        widget_item.setSizeHint(item.sizeHint())
        self.main_ui.messages.addItem(widget_item)
        self.main_ui.messages.setItemWidget(widget_item, item)

    def display_name_jid(self, jid):
        if jid in self.jid_peers:
            return self.display_name(self.jid_peers[jid])
        return 'Unknown {}'.format(jid)

    @staticmethod
    def display_name(peer):
        if isinstance(peer, Group):
            user = peer  # type: Group
            if user.code:
                return "{} ({})".format(user.name, user.code)
            else:
                return user.name
        else:
            group = peer  # type: User
            return "{} ({})".format(group.display_name, group.username)

    def send(self):
        message = self.main_ui.messageEdit.text()
        if self.current_peer:
            kik_client.send(self.current_peer.jid, message)
            if self.current_peer.jid not in config['messages']:
                config['messages'][self.current_peer.jid] = []
            config['messages'][self.current_peer.jid].append({
                'body': message,
                'timestamp': int(time.time() * 1000)
            })
            save_config()
            self.messages_updated(self.current_peer.jid)
            self.main_ui.users.itemWidget(self.main_ui.users.currentItem()).set_last_message_label(message)

        self.main_ui.messageEdit.clear()

    def handle_roster(self, members: List[Peer]):
        self.peers = members
        self.jid_peers = {m.jid: m for m in members}
        self.peers_updated_signal.emit()

    def peers_updated(self):
        self.main_ui.users.clear()
        for member in self.peers:  # type: Group
            item = PeerListItem()
            if member.pic:
                item.set_icon(member.pic + "/thumb.jpg")
            item.set_title_label(self.display_name(member))
            if member.jid in config['messages'] and len(config['messages'][member.jid]) > 0:
                item.set_last_message_label(config['messages'][member.jid][-1]['body'])
            widget_item = QListWidgetItem(self.main_ui.users)
            widget_item.setSizeHint(item.sizeHint())
            self.main_ui.users.addItem(widget_item)
            self.main_ui.users.setItemWidget(widget_item, item)

    def login(self):
        username = self.login_ui.username_edit.text()
        password = self.login_ui.password_edit.text()
        config['username'] = username
        config['password'] = password
        save_config()
        print("Login in as {}:{}".format(username, password))
        kik_client.login(username, password)


class KikCallback(KikClientCallback):
    def on_authorized(self):
        app.on_authorized_signal.emit()

    def on_status_message(self, response: IncomingStatusResponse):
        pass

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        pass

    def on_group_message_received(self, response: IncomingGroupChatMessage):
        if response.from_jid not in config['messages']:
            config['messages'][response.from_jid] = []
        config['messages'][response.from_jid].append(
            {
                'body': response.body,
                'jid': response.from_jid,
                'timestamp': response.metadata.timestamp,
            }
        )
        save_config()
        app.messages_updated_signal.emit(response.group_jid)

    def on_sign_up_ended(self, response: RegisterResponse):
        pass

    def on_peer_info_received(self, response: PeerInfoResponse):
        pass

    def on_friend_attribution(self, response: IncomingFriendAttribution):
        pass

    def on_message_read(self, response: IncomingMessageReadEvent):
        pass

    def on_login_ended(self, response: LoginResponse):
        config['node'] = response.node
        save_config()

    def on_message_delivered(self, response: IncomingMessageDeliveredEvent):
        pass

    def on_group_is_typing_event_received(self, response: IncomingGroupIsTypingEvent):
        pass

    def on_chat_message_received(self, response: IncomingChatMessage):
        if response.from_jid not in config['messages']:
            config['messages'][response.from_jid] = []
        config['messages'][response.from_jid].append(
            {
                'body': response.body,
                'jid': response.from_jid,
                'timestamp': response.metadata.timestamp,
            }
        )
        save_config()
        app.messages_updated_signal.emit(response.from_jid)

    def on_is_typing_event_received(self, response: IncomingIsTypingEvent):
        pass

    def on_group_status_received(self, response: IncomingGroupStatus):
        pass

    def on_group_receipts_received(self, response: IncomingGroupReceiptsEvent):
        pass

    def on_login_error(self, response: LoginError):
        pass

    def on_register_error(self, response: SignUpError):
        pass

    def on_roster_received(self, response: FetchRosterResponse):
        app.handle_roster(response.members)

    def on_connection_failed(self, response: ConnectionFailedResponse):
        if 'node' in config:
            del config['node']
            save_config()
            kik_client.login(config['username'], config['password'])


def save_config():
    global config
    logger.debug("Saving config")
    with open(config_file, 'w') as outfile:
        json.dump(config, outfile)


def load_config():
    global config
    logger.debug("Loading config")
    if not os.path.exists(config_file):
        save_config()
        return
    with open(config_file, 'r') as infile:
        config = json.load(infile)


def main():
    global app
    load_config()
    application = QApplication(sys.argv)
    app = App()
    app.show()

    status = application.exec_()
    kik_client.disconnect()
    sys.exit(status)


if __name__ == '__main__':
    main()
