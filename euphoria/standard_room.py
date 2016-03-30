from . import connection

from . import chat_room

from . import utils

import datetime

class StandardRoom(chat_room.ChatRoom):
    """
    A room with basic utilities already implemented as instructed by
    https://github.com/jedevc/botrulez
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

        self.ping_text = "Pong!"
        self.short_help_text = None
        self.help_text = None

    def handle_message(self, data):
        content = data["data"]["content"]
        reply = data["data"]["id"]
        at_mention = '@' + ''.join(re.split(r'\s', self.nickname))

        if content.lower() == "!ping" or content.lower() == "!ping " + at_mention.lower():
            self.send_chat(self.ping_text, reply)
        elif content.lower() == "!help" and self.short_help_text:
            self.send_chat(self.short_help_text, reply)
        elif content.lower() == "!help " + at_mention.lower() and self.help_text:
            self.send_chat(self.help_text, reply)
        elif content.lower() == "!uptime " + at_mention.lower():
            u = datetime.datetime.strftime(self.start_utc, "%Y-%m-%d %H:%M:%S")
            t = utils.extract_time(self.uptime())

            self.send_chat("/me has been up since " + u + " UTC (" + t + ")", reply)
        else:
            super().handle_message(data)
