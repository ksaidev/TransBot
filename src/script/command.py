from src.structure.doubledict import DoubleDict


class Command:
    REGISTER = 'register'
    HELP_KO, HELP_EN = 'help_ko', 'help_en'
    SET_AUTO, SET_MANUAL = 'set_auto', 'set_manual'
    AUTO_TRANSLATE = 'auto_translate'
    MANUAL_TRANSLATE = 'manual_translate'
    SYNC = 'sync'

    messages = DoubleDict({
        ('도움말',): HELP_KO, ('help',): HELP_EN,
        ('등록', 'reg'): REGISTER,
        ('자동', 'auto', 'ㅈ', 'a'): SET_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): SET_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): MANUAL_TRANSLATE,
        ('동기화', 'sync'): SYNC
    })


    @staticmethod
    def get_type(message):
        if message.startswith('/'):
            command = message[1:]
            return Command.messages[command]

        return Command.AUTO_TRANSLATE
