from kakaoPy import client
from src.script.chat_manager import ChatManager
from src.script.channel_manager import ChannelManager

from data.private import KAKAO_ID, KAKAO_PW


class RootClient(client.Client):
    async def onMessage(self, chat):
        await ChatManager(chat).respond()

    async def onJoin(self, packet, channel):
        await ChannelManager(channel).respond()


root = RootClient("TransBot")
root.run(KAKAO_ID, KAKAO_PW)
