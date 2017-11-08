import sys

from PyQt5.QtCore import QThread, pyqtSignal


class KikThread(QThread):
    received_message = pyqtSignal(str, str)
    received_group_message = pyqtSignal(str, str, str)
    send_message_signal = pyqtSignal(str, str, bool)
    on_login = pyqtSignal()
    message_queue = []
    partners = None

    def __init__(self, kik_client):
        super().__init__()
        self.kik = kik_client
        self.send_message_signal.connect(self.send_message)

    def send_message(self, user, message, groupchat):
        self.message_queue.append([user, message, groupchat])

    def run_queue(self):
        """
        To keep a single duplex socket open, polling is done in a loop with a timeout of 50ms, then all messages in the
        queue are sent.

        TODO: replace this with a more robust / instant mechanism.
        """
        for message in self.message_queue:
            self.kik.send_message(*message)
        self.message_queue.clear()

    def run(self):
        try:
            self.partners = self.kik.get_chat_partners()
            self.on_login.emit()
            while True:
                self.run_queue()
                info = self.kik.get_next_event(0.1)
                if not info:
                    continue
                elif 'type' not in info:
                    print("[-] type not in info")
                    print(info)
                # elif info["type"] == "message_read":
                #     self.message_read(info)
                # elif info["type"] == "is_typing":
                #     self.is_typing(info)
                elif info["type"] == "message":
                    self.received_message.emit(info['from'], info['body'])
                    # self.received_message.emit(info['from'], info['body'])
                elif info['type'] == 'group_message':
                    self.received_group_message.emit(info['group_id'], info['from'], info['body'])
                # elif info['type'] == 'group_typing':
                #     self.group_typing(info)
                # elif info['type'] == 'group_content':
                #     self.group_content(info)
                # elif info['type'] == 'group_sticker':
                #     self.group_sticker(info)
                # elif info['type'] == 'group_gallery':
                #     self.group_gallery(info)
                # elif info['type'] == 'group_camera':
                #     self.group_camera(info)
                # elif info['type'] == 'group_gif':
                #     self.group_gif(info)
                # elif info['type'] == 'group_card':
                #     self.group_card(info)
                # elif info['type'] == 'message':
                #     self.message(info)
                # elif info['type'] == 'content':
                #     self.content(info)
                # elif info['type'] == 'sticker':
                #     self.sticker(info)
                # elif info['type'] == 'gallery':
                #     self.gallery(info)
                # elif info['type'] == 'camera':
                #     self.camera(info)
                # elif info['type'] == 'gif':
                #     self.gif(info)
                # elif info['type'] == 'card':
                #     self.card(info)
                # elif info['type'] == 'qos' or info['type'] == 'acknowledgement':
                #     pass
                # elif info["type"] == "end":
                #     print("[!] Server ended communication.")
                #     break
                else:
                    print("[-] Unknown message of type {}".format(info['type']))
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)
            sys.exit(1)
