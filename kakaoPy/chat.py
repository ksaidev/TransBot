import json
from . import httpApi
import hashlib
import requests


class Chat:
    def __init__(self, channel, body):
        self.channel = channel

        self.rawBody = body

        self.logId = self.rawBody["chatLog"]["logId"]

        self.type = self.rawBody["chatLog"]["type"]

        self.message = self.rawBody["chatLog"]["message"]

        self.msgId = self.rawBody["chatLog"]["msgId"]

        self.authorId = self.rawBody["chatLog"]["authorId"]

        self.chatId = self.channel.chatId

        try:
            if "attachment" in self.rawBody["chatLog"]:
                self.attachment = json.loads(
                    self.rawBody["chatLog"]["attachment"])
            else:
                self.attachment = {}
        except:
            pass

        self.nickName = self.rawBody["chatLog"]["authorId"]


    async def reply(self, msg, t=1):
        return await self.channel.sendChat(msg, json.dumps({
            "attach_only": False,
            "attach_type": t,
            "mentions": [],
            "src_linkId": self.channel.li,
            "src_logId": self.logId,
            "src_mentions": [],
            "src_message": self.message,
            "src_type": self.type,
            "src_userId": self.authorId
        }), 26)

    async def sendChat(self, msg, extra, t):
        return await self.channel.sendChat(msg, extra, t)

    async def sendText(self, msg):
        return await self.channel.sendText(msg)

    async def delete(self):
        return await self.channel.deleteMessage(self.logId)

    async def hide(self):
        return await self.channel.hideMessage(self.logId, self.type)

    async def kick(self):
        return await self.channel.kickMember(self.authorId)

    async def sendPhoto(self, data, w, h):
        path, key, url = httpApi.upload(data, "image/jpeg", self.authorId)
        return await self.channel.forwardChat("", json.dumps({
            "thumbnailUrl": url,
            "thumbnailHeight": w,
            "thumbnailWidth": h,
            "url": url,
            "k": key,
            "cs": hashlib.sha1(data).hexdigest().upper(),
            "s": len(data),
            "w": w,
            "h": h,
            "mt": "image/jpeg"
        }), 2)

    async def sendPhotoPath(self, path, w, h):
        f = open(path, "rb")
        data = f.read()
        f.close()

        return await self.sendPhoto(data, w, h)

    async def sendPhotoUrl(self, url, w, h):
        r = requests.get(url)
        r.raise_for_status()

        return await self.sendPhoto(r.content, w, h)

    async def sendLongText(self, title, content):
        path, key, url = httpApi.upload(
            content.encode("utf-8"), "image/jpeg", self.authorId)

        return await self.channel.forwardChat(title, json.dumps({"path": path, "k": key, "s": len(content), "cs": "", "sd": True}), 1)

    # custom methods
    async def sendTexts(self, msg_list):
        for msg in msg_list:
            await self.sendText(msg)

