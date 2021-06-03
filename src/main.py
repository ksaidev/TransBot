# from kakaoPy import client
from KakaoBot.kakaopy.client import Client
from src.bot.responder.chat import ChatResponder
from src.bot.responder.channel import ChannelResponder
from src.bot.logging import Logging

from data.private import KAKAO_ID, KAKAO_PW, DEVICE_NAME, DEVICE_UUID


class BotClient(Client):
    async def on_message(self, chat):
        await chat.read()
        await ChatResponder(chat).respond()

    async def on_join(self, packet, channel):
        await ChannelResponder(channel).respond()

def run():
    bot = BotClient(DEVICE_NAME, DEVICE_UUID)
    bot.loop.set_exception_handler(Logging.exception_handler)
    bot.run(KAKAO_ID, KAKAO_PW)
