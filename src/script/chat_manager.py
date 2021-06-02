from src.script.command import CommandType
from src.script.channel_manager import ChannelManager
from src.script.exceptions import BotException, ModeSetError, ManualSelectionError
from src.constants import messages
from src.constants.mode import Mode
from src.script.translator import Translator
from src.data.word_db import WordDatabase


class ChatManager:
    """
    An object generated for each message received for
    registration, managing current modes, and replying, etc.
    Contains the message channel instance, message/attachments text, etc.
    """
    translator = Translator()
    database = WordDatabase()

    def __init__(self, chat):
        self.channel = ChannelManager(chat.channel)
        self.message = chat.message
        self.type = chat.type
        self.attachment = chat.attachment['src_message'] if chat.type == 26 else None
        self.mode = self.channel.get_mode()

    async def respond(self):
        """
        Root function that responds to a user message
        """
        if not self.channel.is_registered():
            self.channel.register()

        if not self.translatable():
            return

        command = CommandType.get_type(self.message, self.channel.is_admin())
        try:
            await self.run_command(command)
        except BotException as error:
            await self.send_text(error.notify_message)


    async def run_command(self, command):
        """
        Runs a command function by its name
        The Command functions are functions decorated by '@Command()'
        """
        return await getattr(self, command)()

    async def send_text(self, text):
        """
        Sends a text message in the channel where the input message was sent
        """
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
        def __init__(self, exceptions=None):
            self.exceptions = {} if exceptions is None else exceptions

        def __call__(self, func):
            def command_func(obj):
                # mode = obj.channel.get_mode()

                if obj.mode in self.exceptions:
                    raise self.exceptions[obj.mode]

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

    @Command()
    async def plain_respond(self):
        """
        Translates the message and sends back the translated message
        Only works on auto mode
        """
        if self.mode == Mode.AUTO:
            translated_text = self.translator.translate(self.message)
            header = '[Auto Translation]\n'
            await self.send_text(header + translated_text)

    @Command()
    async def manual_translate(self):
        """
        Manually translates the attached message and sends back the the translated message
        Works on both modes
        """
        if self.attachment is None:
            raise ManualSelectionError
        header = '[Manual Translation]\n'
        translated_text = self.translator.translate(self.attachment)
        await self.send_text(header + translated_text)


    @Command()
    async def sync(self):
        """
        Pulls the word database from the remote database and syncs it with the local database
        Sends back the rows with errors
        Only works in admin channels
        """
        await self.send_text(messages.SYNC_START)
        error_data = self.database.pull()

        sheet_name = {'ksa_words': 'ksa_words',
                      'target_ko': 'general(en→ko)',
                      'target_en': 'general(en→ko)'}
        for sheet_key in error_data:
            errors = error_data[sheet_key]
            if len(errors) > 0:
                error_message = f'error in sheet [{sheet_name[sheet_key]}]'
                for row in errors:
                    error = '[blank cell]' if errors[row] == '' else f"'{errors[row]}'"
                    error_message += f'\n{row} {error}'
                await self.send_text(error_message)

        await self.send_text(messages.SYNC_COMPLETE)

    @Command()
    async def restart(self):
        await self.send_text(messages.RESTART)
        raise ConnectionResetError
