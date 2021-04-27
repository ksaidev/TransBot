from src.script.command import Command
from src.script.admin_command import AdminCommand
from src.script.channel_manager import ChannelManager
from src.script.exceptions import BotException, ModeSetError, ManualSelectionError
from src.constants import messages
from src.constants.mode import Mode
from src.script.translator import Translator


class ChatManager:
    translator = Translator()

    def __init__(self, chat):
        self.channel = ChannelManager(chat.channel)
        self.message = chat.message
        self.type = chat.type
        self.attachment = chat.attachment['src_message'] if chat.type == 26 else None
        if chat.channel.is_admin():
            self.command = AdminCommand.get_type(self.message)
        else:
            self.command = Command.get_type(self.message)

    async def respond(self):
        if not self.channel.is_registered():
            self.channel.register()

        if not self.translatable():
            return

        try:
            await self.run_command()
        except BotException as error:
            await self.send_text(error.notify_message)


    async def run_command(self):
        return getattr(self, self.command)()

    async def send_text(self, text):
        await self.channel.send_text(text)


    def translatable(self):
        """
        Checks if the message type is translatable
        """
        if self.message == '':
            return False
        return True if self.type in (1, 20, 26) else False


    class Command:
        """
        A command decorator that decorates the command functions
        """
        def __init__(self, exceptions=None, ignore=None):
            self.exceptions = {} if exceptions is None else exceptions
            self.ignore = ignore

        def __call__(self, func):
            def command_func(obj):
                mode = obj.channel.get_mode()

                if mode in self.exceptions:
                    raise self.exceptions[mode]

                if mode != self.ignore:
                    return func(obj)

            return command_func


    @Command()
    async def help_ko(self):
        """
        sends a help message in Korean
        """
        await self.send_text(messages.HELP_KOR)


    @Command()
    async def help_en(self):
        """
        sends a help message in English
        """
        await self.send_text(messages.HELP_ENG)


    @Command(exceptions={Mode.AUTO: ModeSetError(Mode.AUTO)})
    async def set_auto(self):
        """
        Sets a channel in auto mode
        Sends a error message if the channel is already in auto mode
        """
        self.channel.set_mode(Mode.AUTO)
        await self.send_text(messages.SET_AUTO)


    @Command(exceptions={Mode.MANUAL: ModeSetError(Mode.MANUAL)})
    async def set_manual(self):
        """
        Sets a channel in manual mode
        Sends a error message if the channel is already in manual mode
        """
        self.channel.set_mode(Mode.MANUAL)
        await self.send_text(messages.SET_MANUAL)

    @Command(ignore=Mode.MANUAL)
    async def auto_translate(self):
        translated_text = self.translator.translate(self.message)
        header = '[Auto Translation]\n'
        await self.send_text(header + translated_text)


    @Command()
    async def manual_translate(self):
        if self.attachment is None:
            raise ManualSelectionError
        header = '[Manual Translation]\n'
        translated_text = self.translator.translate(self.attachment)
        await self.send_text(header + translated_text)


    @Command()
    async def sync(self):
        pass

    # 관리자 명령어는 Command class 를 inherit 해서 AdminCommand 를 만들던지
    # 아니면 responder 상속해서 하덩가





