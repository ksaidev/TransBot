from src.script.command import Command
from src.script.channel import BotChannel
from src.script.exceptions import *
from src.constants import messages
from src.constants.mode import Mode


class Responder:
    def __init__(self, chat):
        self.channel = BotChannel(chat.channel)
        if self.channel.is_admin():
            self.command = Command.get_function(chat.message, admin=True)
        else:
            self.command = Command.get_function(chat.message)


    async def respond(self):
        try:
            await self.command(self)
        except BotException as error:
            await self.send_text(error.notify_message)


    async def send_text(self, text):
        await self.channel.sendText(text)


    @Command(Command.REGISTER, allow_unregistered=True)
    async def _register(self):
        if self.channel.mode != Mode.UNREGISTERED:
            raise RegistrationError(registered=True)

        self.channel.register()
        await self.send_text(messages.WELCOME)


    @Command(Command.HELP_KO)
    async def _help_ko(self):
        # if not self.channel.is_registered():
        #     raise exceptions.RegistrationError(registered=False)

        await self.send_text(messages.HELP_KOR)


    @Command(Command.HELP_EN)
    async def _help_en(self):
        # if not self.channel.is_registered():
        #     raise exceptions.RegistrationError(registered=False)

        await self.send_text(messages.HELP_ENG)


    @Command(Command.SET_AUTO,
             exceptions={Mode.AUTO: ModeSetError(Mode.AUTO)})
    async def _set_auto(self):
        self.channel.set_mode(Mode.AUTO)
        await self.send_text(messages.SET_AUTO)


    @Command(Command.SET_MANUAL,
             exceptions={Mode.MANUAL: ModeSetError(Mode.MANUAL)})
    async def _set_manual(self):
        self.channel.set_mode(Mode.MANUAL)
        await self.send_text(messages.SET_MANUAL)


    @Command(Command.AUTO_TRANSLATE)
    async def _auto_translate(self):
        if not self.channel.is_registered():
            raise exceptions.RegistrationError(registered=False)

    @Command(Command.MANUAL_TRANSLATE)
    async def _manual_translate(self):
        if not self.channel.is_registered():
            raise exceptions.RegistrationError(registered=False)

    @Command(Command.SYNC)
    async def _sync(self):
        if not self.channel.is_registered():
            raise exceptions.RegistrationError(registered=False)








if __name__ == '__main__':
    def is_unregistered():
        return False

    class Chat:
        def __init__(self, message):
            self.message = message
            self.channel = None
            self.channel.is_unregistered = is_unregistered

    chat_obj = Chat('/ㅅ')
    responder = Responder(chat_obj)

    responder._run_command()
