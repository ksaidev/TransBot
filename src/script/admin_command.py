from src.module.doubledict import DoubleDict
from src.script.command import Command

class AdminCommand(Command):
    """
    Contains the admin commands and command types of TransBot
    which will only work in admin channels
    """
    SYNC = 'sync'

    messages = DoubleDict({
        ('동기화', 'sync'): SYNC
    })

    @staticmethod
    def get_type(message):
        """
        Returns the command type from the message text
        Returns non-admin commands from Command module if no commands are matched
        """
        if message.startswith('/'):
            command = message[1:]
            if command in AdminCommand.messages:
                return AdminCommand.messages[command]

        return super().get_type(message)
