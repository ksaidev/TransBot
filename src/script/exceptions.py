from src.constants import messages
from src.constants.mode import Mode
from src.script.logging import Logging


class BotException(Exception):
    """
    An abstract class to handle errors of the bot.
    Each BotException should have a error notifier message which will be delivered to the user.
    When raised, the error notifier message is sent to the user
    """
    def __init__(self, notify_message):
        super().__init__()
        self.notify_message = notify_message

class ModeSetError(BotException):
    """
    An error raised when the user tries to change the mode into the current mode
    """
    def __init__(self, mode):
        assert mode in (Mode.AUTO, Mode.MANUAL)
        notify_message = messages.ERROR_ALREADY_AUTO if mode == Mode.AUTO \
            else messages.ERROR_ALREADY_MANUAL
        super().__init__(notify_message)

class ManualSelectionError(BotException):
    """
    An error raised when the attachment message is not selected in manual translation
    """
    def __init__(self):
        super().__init__(messages.ERROR_MSG_UNSELECTED)

class ApiLimitExceeded(BotException):
    """
    An error raised when the Papago API limit is exceeded
    """
    def __init__(self):
        Logging.console('API limit exceeded')
        super().__init__(messages.ERROR_API_LIMIT_EXCEEDED)

class KeywordTranslationError(BotException):
    """
    An error raised when the keyword match is not found during postprocessing
    """
    def __init__(self):
        Logging.console('Keyword translation error')
        super().__init__(messages.ERROR_KEYWORD_UNMATCHED)

class UndefinedError(BotException):
    """
    An error to wrap undefined general exceptions
    """
    def __init__(self):
        Logging.console('Undefined error')
        super().__init__(messages.ERROR_UNDEFINED)
