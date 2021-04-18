from kakaoPy import client
import admin

import bot
import message
from channel import Channel
from data import private

class RootClient(client.Client):
    async def onMessage(self, chat):
        # if chat.type not in (1, 26):
        #     return

        # TODO
        # Channel 객체를 만들어서 데이터베이스와 연동?
        # kakaoPy send by chatId 만들면 연동
        channel = Channel(chat)

        if channel.isRegistered():
            if admin.syncStart(chat):
                await chat.sendText(message.syncStart)
                logs = admin.sync_log()
                await chat.sendTexts(logs)

            else:
                messages = bot.respond(chat)
                await chat.sendTexts(messages)

        else:
            messages = bot.register(chat)
            await chat.sendTexts(messages)


client = RootClient("TransBot")
client.run(private.kakao_id, private.kakao_pw)
