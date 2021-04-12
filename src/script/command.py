class Command:
    class Type:
        def __init__(self, name):
            self.__name = name

        def __hash__(self):
            return hash(self.__name)

        def __eq__(self, other):
            return self.__name == other.__name

    REGISTER = Type('register')
    HELP_KO, HELP_EN = Type('help_ko'), Type('help_en')
    SET_AUTO, SET_MANUAL = Type('set_auto'), Type('set_manual')
    AUTO_TRANSLATE = Type('auto_translate')
    MANUAL_TRANSLATE = Type('manual_translate')

    SYNC = Type('sync')

    settings = {
        ('도움말',): HELP_KO, ('help',): HELP_EN,
        ('등록', 'reg'): REGISTER,
        ('자동', 'auto', 'ㅈ', 'a'): SET_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): SET_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): MANUAL_TRANSLATE
    }

    admin_settings = {
        ('동기화', 'sync'): SYNC
    }

    functions = dict()

    def __init__(self, command_type):
        self.command_type = command_type

    def __call__(self, command_func):
        self.functions[self.command_type] = command_func
        return command_func

    @staticmethod
    def _get_type(message, is_admin):
        if message.startswith('/'):
            command = message[1:]
            if is_admin:
                for admin_commands in Command.admin_settings:
                    if command in admin_commands:
                        return Command.admin_settings[admin_commands]

            for commands in Command.settings:
                if command in commands:
                    return Command.settings[commands]
        return Command.AUTO_TRANSLATE

    @staticmethod
    def get_function(message, admin=False):
        command_type = Command._get_type(message, admin)
        return Command.functions[command_type]
