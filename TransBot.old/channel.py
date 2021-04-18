from src.data.channel_db import ChannelDatabase

class Channel:
    db = ChannelDatabase()

    def __init__(self, chat):
        channel = chat.channel
        self._channel = channel
        self.chatId = channel.chatId


    async def sendText(self, msg):
        await self._channel.sendText(msg)


    def setMode(self, mode):
        assert mode in ('auto', 'manual')
        Channel.db.setMode(self.chatId, mode)


    def isRegistered(self):
        return Channel.db.isRegistered(self.chatId)


    def isAutoMode(self):
        return Channel.db.isAutoMode(self.chatId)
