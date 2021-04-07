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

        '''
        wr = chat.channel.writer
        print(wr.crypto)
        print(wr.StreamWriter)
        print(wr.PacketID)
        print(wr.PacketDict)
        238173194189938 0
        299273051922895 0
        '''

        if chat.message == "와":
            await chat.reply("샌주")
        
        '''#자신 메시지만
        if chat.message == ".삭제":
            await chat.delete()
        
        #OpenChat 권한 있을떄
        if chat.message == ".가리기":
            await chat.hide()
            
        if chat.message == '테스트':
            await chat.sendText('ㅎㅇ')

        if chat.type == 26:
            msg = chat.attachment['src_message']
            await chat.sendText(msg)

        if chat.type == 2:
            att = chat.attachment
            url, w, h = att['url'], att['w'], att['h']

            await chat.sendPhotoUrl(url, w, h)

        if chat.message == 'ㅇ':
            client.postText(299273051922895, 0, '공지', True)

        if chat.type == 18:
            await chat.channel.sendChat('', json.dumps(chat.attachment), 18)

        if chat.message == '임티':
            await chat.channel.sendChat('', json.dumps({'name': '(이모티콘)', 'path': '4414774.emot_001.webp', 'type': 'image/webp', 's': 0, 'alt': '카카오 이모티콘'}), 20)


    async def onJoin(self, packet, channel):
        await channel.sendText('초대됨')'''





client = MyClass("DEVICE")
client.run("rnjstnsgh3368@gmail.com", "rnjstnsgh0115")
