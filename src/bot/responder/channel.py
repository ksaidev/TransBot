from src.data.channel_db import ChannelDatabase
from data.private import ADMIN_CHANNEL
from src.constants import messages

class ChannelResponder:
    """
    An object for managing channels
    Called directly on join and included in chat object as instance variable on message
    Contains channel instance and channel uid for accessing channel database
    """
    database = ChannelDatabase()

    def __init__(self, channel):
        self.channel = channel
        self.chat_id = channel.chat_id

    async def respond(self):
        """
        Called when TransBot has joined a new room
        Registers the channel uid in the channel database
        Sends a welcome message
        """
        if self.is_registered():
            return

        self.register()
        await self.send_text(messages.WELCOME)


    def is_registered(self):
        return self.get_mode() is not None

    def register(self):
        """
        Appends the channel uid in the channel database
        The initial mode is Mode.AUTO = 1
        """
        self.database.add_channel(self.chat_id)

    def get_mode(self):
        """
        Gets the mode of the current channel
        Mode.AUTO = 1, Mode.AUTO = 0
        returns None if unregistered
        """
        return self.database.get_mode(self.chat_id)

    def set_mode(self, mode):
        self.database.set_mode(self.chat_id, mode)

    def is_admin(self):
        return self.chat_id in ADMIN_CHANNEL

    async def send_text(self, message):
        await self.channel.send_text(message)
