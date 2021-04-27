import sqlite3


class Database:
    def __init__(self, dir):
        self._dir = dir
        self._connection = None
        self._cursor = None

    @staticmethod
    def connection(func):
        def wrapper(self, *args, **kwargs):
            self._connect()
            try:
                result = func(self, *args, **kwargs)
            finally:
                self._close()
            return result
        return wrapper

    def _connect(self):
        assert self._connection is None and self._cursor is None
        self._connection = sqlite3.connect(self._dir)
        self._cursor = self._connection.cursor()

    def _close(self):
        assert self._connection is not None and self._cursor is not None
        self._connection.close()
        self._cursor, self._connection = None, None

    # def _write_command(self, command):
    #     assert self._cursor is not None
    #     self._cursor.execute(command)

    def execute(self, *args):
        assert self._cursor is not None
        self._cursor.execute(*args)

    def fetch(self):
        assert self._cursor is not None
        return self._cursor.fetchall()

    # def command(self, command):
    #     self._connect()
    #     self._execute(command)
    #     result = self._fetch()
    #     self._close()
    #
    #     return result




