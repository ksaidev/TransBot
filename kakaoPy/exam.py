import client
from packet import Packet
import bson
import time
import json

class MyClass(client.Client):
    """
    async def onPacket(self, packet):
        name = packet.PacketName
        body = packet.toJsonBody()
        # print(name)
        print(body)
        # print("\n")
    """


    async def onMessage(self, chat):
        #print(chat.channel.chatId, chat.channel.li)
        print(chat.message)
        print(chat.type)
        print(chat.attachment)

        if chat.message == "와":
            await chat.reply("샌주")
        



client = MyClass("DEVICE")
client.run("rnjstnsgh3368@gmail.com", "rnjstnsgh0115")
