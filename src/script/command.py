from src.module.doubledict import DoubleDict


class CommandType:
    """
    Contains the commands and command types of TransBot
    """
    HELP_KO, HELP_EN = 'help_ko', 'help_en'
    SET_AUTO, SET_MANUAL = 'set_auto', 'set_manual'
    MANUAL_TRANSLATE = 'manual_translate'
    SYNC = 'sync'
    RESTART = 'restart'
    PLAIN_RESPOND = 'plain_respond'

    messages = DoubleDict({
        ('도움말',): HELP_KO, ('help',): HELP_EN,
        ('자동', 'auto', 'ㅈ', 'a'): SET_AUTO,
        ('수동', 'manual', 'ㅅ', 'm'): SET_MANUAL,
        ('번역', 'translate', 'ㅂ', 'tr'): MANUAL_TRANSLATE,
    })

    admin_messages = DoubleDict({
        ('동기화', 'sync'): SYNC,
        ('재시작', 'restart'): RESTART
    })


    @staticmethod
    def get_type(message, is_admin=False):
        """
        Returns the command type from the message text
        Returns CommandType.AUTO_TRANSLATE if no commands are matched
        """
        if message.startswith('/'):
            command = message[1:]
            if is_admin and command in CommandType.admin_messages:
                return CommandType.admin_messages[command]

            if command in CommandType.messages:
                return CommandType.messages[command]

        return CommandType.PLAIN_RESPOND
