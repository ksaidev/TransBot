from src.constants import message


class BotException(Exception):
    def __init__(self, notify_message):
        super().__init__()
        self.notify_message = notify_message


class RegistrationError(BotException):
    def __init__(self, registered):
        notify_message = message.ERROR_REGISTERED if registered \
            else message.ERROR_UNREGISTERED
        super().__init__(notify_message)

class ModeSetError(BotException):
    def __init__(self, mode):
        assert mode in ('auto', 'manual')
        notify_message = message.ERROR_ALREADY_AUTO if mode == 'auto' \
            else message.ERROR_ALREADY_MANUAL
        super().__init__(notify_message)

class ManualSelectionError(BotException):
    def __init__(self):
        super().__init__(message.ERROR_MSG_UNSELECTED)

