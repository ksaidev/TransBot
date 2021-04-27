from src.module.doubledict import DoubleDict
from src.script.command import Command

class AdminCommand(Command):
    SYNC = 'sync'

    messages = DoubleDict({
        ('동기화', 'sync'): SYNC
    })

    @staticmethod
    def get_type(message):
        if message.startswith('/'):
            command = message[1:]
            if command in AdminCommand.messages:
                return AdminCommand.messages[command]

        return super().get_type(message)
