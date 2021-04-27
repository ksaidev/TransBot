from src.module.doubledict import DoubleDict
from src.script.exceptions import *

class Command:
    class Type:
        def __init__(self, name):
            self.__name = name

        def __hash__(self):
            return hash(self.__name)

        def __eq__(self, other):
            return self.__name == other.__name

    # Command Type Constants
    REGISTER = Type('register')
    HELP_KO, HELP_EN = Type('help_ko'), Type('help_en')
    SET_AUTO, SET_MANUAL = Type('set_auto'), Type('set_manual')
    AUTO_TRANSLATE = Type('auto_translate')
    MANUAL_TRANSLATE = Type('manual_translate')
    SYNC = Type('sync')


    settings = DoubleDict({
        ('도움말',): HELP_KO, ('help',): HELP_EN,
        ('등록', 'reg'): REGISTER,
        ('자동', 'auto', 'ㅈ', 'a'): SET_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): SET_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): MANUAL_TRANSLATE,
        ('동기화', 'sync'): SYNC
    })

    functions = dict()

    def __init__(self, command_type, allow_unregistered=False):
        self.command_type = command_type
        self.allow_unregistered = allow_unregistered


    def __call__(self, func):
        def command_func(responder):
            if not self.allow_unregistered:
                if responder.channel.mode == Mode.UNREGISTERED:
                    raise RegistrationError(registered=False)

            return func(responder)

        self.functions[self.command_type] = command_func
        return command_func

    @staticmethod
    def _get_type(message):
        if message.startswith('/'):
            command = message[1:]
            return Command.settings[command]

        return Command.AUTO_TRANSLATE

    @staticmethod
    def get_function(message):
        command_type = Command._get_type(message)
        return Command.functions[command_type]
