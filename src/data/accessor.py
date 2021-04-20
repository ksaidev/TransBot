import sqlite3



# def connection(func, *args, **kwargs):
#     def wrapper(self):
#         self._connect()
#         func(*args, **kwargs)
#         self._close()
#     return wrapper


class Database:
    def __init__(self, dir):
        self._dir = dir

    def _write_command(self, command):
        conn = sqlite3.connect(self._dir)
        c = conn.cursor()

        c.execute(command)

        conn.commit()
        conn.close()

    def _read_command(self, command):
        conn = sqlite3.connect(self._dir)
        c = conn.cursor()

        c.execute(command)
        result = c.fetchall()

        conn.close()
        return result


    # def _connect(self):
    #     self.connection = sqlite3.connect(self._dir)
    #     self.cursor = self.connection.cursor()
    #
    # def _close(self):
    #     self.connection.commit()
    #     self.connection.close()
    #


