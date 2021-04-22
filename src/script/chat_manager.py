from src.script.command import Command
from src.script.channel import BotChannel
from src.script.exceptions import *
from src.constants import messages
from src.constants.mode import Mode


class Responder:
    def __init__(self, chat=None, channel=None):
        if chat is None:
            self.channel = BotChannel(channel)
            self.message = None

        else:
            self.channel = BotChannel(chat.channel)
            self.message = chat.message
            self.command = Command.get_type(self.message)
            self.attachments = None #TODO

    async def on_message(self):
        try:
            await self.run_command()
        except BotException as error:
            await self.send_text(error.notify_message)

    async def on_join(self):
        pass


    async def run_command(self):
        return getattr(self, self.command)()

    async def send_text(self, text):
        await self.channel.sendText(text)


    class Command:
        """
        A command decorator that decorates the command functions
        Handles the scope of the command
        """
        def __init__(self, scope=(), exceptions=None):
            self.scope = scope
            self.exceptions = dict() if exceptions is None else exceptions

        def __call__(self, func):
            def command_func(obj):
                mode = obj.channel.mode

                if mode in self.exceptions:
                    raise self.exceptions[mode]

                if mode in self.scope:
                    return func(obj)

            return command_func


    @Command(scope=(Mode.UNREGISTERED,),
             exceptions={Mode.AUTO: RegistrationError(registered=True),
                         Mode.MANUAL: RegistrationError(registered=True)})
    async def register(self):
        # if self.channel.mode != Mode.UNREGISTERED:
        #     raise RegistrationError(registered=True)

        self.channel.register()
        await self.send_text(messages.WELCOME)


    @Command(scope=(Mode.AUTO, Mode.MANUAL))
    async def help_ko(self):
        await self.send_text(messages.HELP_KOR)


    @Command(scope=(Mode.AUTO, Mode.MANUAL))
    async def help_en(self):
        await self.send_text(messages.HELP_ENG)


    @Command(scope=(Mode.MANUAL,),
             exceptions={Mode.AUTO: ModeSetError(Mode.AUTO)})
    async def set_auto(self):
        # if self.channel.mode == Mode.AUTO:
        #     raise ModeSetError(Mode.AUTO)

        self.channel.set_mode(Mode.AUTO)
        await self.send_text(messages.SET_AUTO)

    @Command(scope=(Mode.AUTO,),
             exceptions={Mode.MANUAL: ModeSetError(Mode.MANUAL)})
    async def set_manual(self):
        # if self.channel.mode == Mode.MANUAL:
        #     raise ModeSetError(Mode.MANUAL)

        self.channel.set_mode(Mode.MANUAL)
        await self.send_text(messages.SET_MANUAL)

    @Command(scope=(Mode.AUTO,))
    async def auto_translate(self):
        if self.channel.mode == Mode.MANUAL:
            return

        # main script goes here

    @Command(scope=(Mode.AUTO, Mode.MANUAL))
    async def manual_translate(self):
        # 자동일때도 작동되네



    @Command(scope=(Mode.AUTO, Mode.MANUAL))
    async def sync(self):
        if not self.channel.is_admin():
            await self.auto_translate()











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
