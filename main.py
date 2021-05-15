from kakaoPy import client
import admin

import bot
import text
from DB import mode
import private

import time

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


while True:
    try:
        client = MyClass("TransBot")
        client.run(private.kakao_id, private.kakao_pw)
    except Exception as e:
        print(e)
        client.loop.close()

    time.sleep(5)
    print('=======================')
