from src.module.doubledict import DoubleDict


class Command:
    # names of command functions in responder.py
    HELP_KO, HELP_EN = 'help_ko', 'help_en'
    SET_AUTO, SET_MANUAL = 'set_auto', 'set_manual'
    AUTO_TRANSLATE = 'auto_translate'
    MANUAL_TRANSLATE = 'manual_translate'

    messages = DoubleDict({
        ('도움말',): HELP_KO, ('help',): HELP_EN,
        ('자동', 'auto', 'ㅈ', 'a'): SET_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): SET_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): MANUAL_TRANSLATE,
    })


    @staticmethod
    def get_type(message):
        if message.startswith('/'):
            command = message[1:]
            if command in Command.messages:
                return Command.messages[command]

        return Command.AUTO_TRANSLATE
