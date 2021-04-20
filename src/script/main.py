from kakaoPy import client
from src.script.responder import Responder


class RootClient(client.Client):
    async def onMessage(self, chat):
        responder = Responder(chat)
        await responder.respond()




root = RootClient("TransBot")
root.run(id, pw)


