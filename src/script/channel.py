from kakaoPy.channel import Channel
from src.data.channel_db import ChannelDatabase
from data.private import ADMIN_CHANNEL

class BotChannel(Channel):
    database = ChannelDatabase()

    def __init__(self, channel):
        super().__init__(channel.chatId, channel.li, channel.writer)
        self.chat_id = channel.chatId
        self.mode = self.get_mode()

    # def is_registered(self):
    #     return self.mode is not None

    def register(self):
        self.database.add_channel(self.chat_id)

    def get_mode(self):
        return self.database.get_mode(self.chat_id)

    def set_mode(self, mode):
        self.database.set_mode(self.chat_id, mode)

    def is_admin(self):
        return self.chat_id in ADMIN_CHANNEL
