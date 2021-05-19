from kakaoPy import client
import admin

import bot
import text
from DB import mode
import private


class MyClass(client.Client):
    async def onMessage(self, chat):
        if chat.type in [1, 26]:
            if mode.isRegistered(chat):

                if admin.syncStart(chat):
                    await chat.sendText(text.syncStart)
                    logs = admin.sync_log()
                    await chat.sendTexts(logs)

                else:
                    messages = bot.respond(chat)
                    await chat.sendTexts(messages)

            else:
                messages = bot.register(chat)
                await chat.sendTexts(messages)


def run():
    trans_bot = MyClass("TransBot")
    trans_bot.run(private.kakao_id, private.kakao_pw)
