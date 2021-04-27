from src.data.channel_db import ChannelDatabase
from data.private import ADMIN_CHANNEL
from src.constants import messages

class ChannelManager:
    database = ChannelDatabase()

    def __init__(self, channel):
        self.channel = channel
        self.chat_id = channel.chatId

    async def respond(self):
        if self.is_registered():
            return

        self.register()
        await self.send_text(messages.WELCOME)


    def is_registered(self):
        return self.get_mode() is not None

    def register(self):
        self.database.add_channel(self.chat_id)

    def get_mode(self):
        return self.database.get_mode(self.chat_id)

    def set_mode(self, mode):
        self.database.set_mode(self.chat_id, mode)

    def is_admin(self):
        return self.chat_id in ADMIN_CHANNEL

    async def send_text(self, message):
        await self.channel.sendText(message)
