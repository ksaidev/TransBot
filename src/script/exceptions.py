from src.constants import messages
from src.constants.mode import Mode

class BotException(Exception):
    def __init__(self, notify_message):
        super().__init__()
        self.notify_message = notify_message


class RegistrationError(BotException):
    def __init__(self, registered):
        notify_message = messages.ERROR_REGISTERED if registered \
            else messages.ERROR_UNREGISTERED
        super().__init__(notify_message)

class ModeSetError(BotException):
    def __init__(self, mode):
        assert mode in (Mode.AUTO, Mode.MANUAL)
        notify_message = messages.ERROR_ALREADY_AUTO if mode == Mode.AUTO \
            else messages.ERROR_ALREADY_MANUAL
        super().__init__(notify_message)

class ManualSelectionError(BotException):
    def __init__(self):
        super().__init__(messages.ERROR_MSG_UNSELECTED)


__all__ = [BotException, RegistrationError, ModeSetError, ManualSelectionError]
