# from kakaoPy import client
from KakaoBot.kakaopy.client import Client
from src.script.chat_manager import ChatManager
from src.script.channel_manager import ChannelManager
from src.script.logging import Logging

from data.private import KAKAO_ID, KAKAO_PW, DEVICE_NAME, DEVICE_UUID


class BotClient(Client):
    async def on_message(self, chat):
        await chat.read()
        await ChatManager(chat).respond()

    async def on_join(self, packet, channel):
        await ChannelManager(channel).respond()

def run():
    bot = BotClient(DEVICE_NAME, DEVICE_UUID)
    bot.loop.set_exception_handler(Logging.exception_handler)
    bot.run(KAKAO_ID, KAKAO_PW)
