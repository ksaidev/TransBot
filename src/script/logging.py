from datetime import datetime
from pprint import pprint

class Logging:
    @classmethod
    def console(cls, log_msg):
        print(f'{cls.current_timestamp()} {log_msg}')

    @staticmethod
    def current_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def exception_handler(cls, loop, context):
        exception = context.get('exception')
        if isinstance(exception, ConnectionResetError):
            cls.console('Connection reset')
            loop.stop()
        elif isinstance(exception, Exception):
            cls.console('Undefined error')
            pprint(context)
            loop.stop()
