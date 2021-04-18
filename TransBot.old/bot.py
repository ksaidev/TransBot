from src.data import channel_db
from src.data.channel_db import ChannelDatabase
from src.language.interpret import interpreter

import message


class Bot:
    COMMAND_HELP_KO, COMMAND_HELP_EN = 'help_ko', 'help_en'
    COMMAND_REGISTER = 'reg'
    COMMAND_AUTO, COMMAND_MANUAL = 'auto', 'manual'
    COMMAND_TRANSLATE = 'tr'

    commands = {
        ('도움말',): COMMAND_HELP_KO,
        ('help',): COMMAND_HELP_EN,
        ('등록', 'reg'): COMMAND_REGISTER,
        ('자동', 'auto', 'ㅈ', 'a'): COMMAND_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): COMMAND_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): COMMAND_TRANSLATE
    }

    class Chat:
        def __init__(self, chat):
            assert chat.type in (1, 26)
            self.message = chat.message

        def command(self):
            if not self.message.startswith('/'):
                return None
            line = self.message[1:]

            for commands in Bot.commands:
                if line in commands:
                    return Bot.commands[commands]
            return None


    class Channel:
        db = ChannelDatabase()

        def __init__(self, chat):
            channel = chat.channel
            self._channel = channel
            self.chatId = channel.chatId

        async def sendText(self, msg):
            await self._channel.sendText(msg)

        def setMode(self, mode):
            assert mode in ('auto', 'manual')
            self.db.setMode(self.chatId, mode)

        def isRegistered(self):
            return self.db.isRegistered(self.chatId)

        def isAutoMode(self):
            return self.db.isAutoMode(self.chatId)

        def isAdmin(self):
            pass


    def __init__(self, chat):
        self.chat = self.Chat(chat)
        self.channel = self.Channel(chat)


    def onMessage(self, chat):
        if chat.type not in (1, 26):
            return





def respond(chat):


    chatId = chat.channel.chatId
    message = chat.message

    # Always works (regardless of mode)
    if message == '/도움말':
        return [message.korHelpMsg]
    if message == '/help':
        return [message.engHelpMsg]
    if message in ['/등록', '/reg']:
        return [message.alreadyRegistered]

    # Mode change
    if message in ['/수동', '/ㅅ', '/manual', '/m']:
        if channel_db.isActivated(chat):
            channel_db.deactivate(chatId)
            return [message.changeToManual]

        else:
            return [message.alreadyManual]

    if message in ['/자동', '/ㅈ', '/auto', '/a']:
        if channel_db.isActivated(chat):
            return [message.alreadyAuto]

        else:
            channel_db.activate(chatId)
            return [message.changeToAuto]

    # Manual Translation
    if message in ['/번역', '/ㅂ', '/translate', '/tr']:
        if chat.type == 26:
            extra = chat.attachment

            msg = extra['src_message']
            res = interpreter(msg)

            # TODO
            '''
            if extra['attach_type'] in [1, 26]:


            else:
            '''

            return ['[Manual Translate] ' + res]

        else:
            return [message.ManualSelectionError]

    # Auto Translation
    if channel_db.isActivated(chat):
        res = interpreter(chat.message)
        return ['[Auto Translate] ' + res]

    return []


def register(chat):
    message = chat.message
    chatId = chat.chatId

    if message in ['/등록', '/reg', '/register']:
        channel_db.activate(chatId)

        return message.welcomeMsg

    else:
        # TODO : 이 메시지 한번만 출력되게 하기 - Database
        return [message.registrationReq]


def translatable(chat):
    if chat.type in [1, 26]:
        return True

    message = chat.message
    # TODO
