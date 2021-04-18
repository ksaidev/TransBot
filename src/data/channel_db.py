import sqlite3

class ChannelDatabase:
    def __init__(self, dir='./database/channel.db'):
        self._dir = dir

    def _readStatus(self, chatId):
        conn = sqlite3.connect(self._dir)
        c = conn.cursor()

        c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')
        res = c.fetchone()

        conn.close()
        return res[0] if res is not None else None


    def _writeStatus(self, chatId, status):
        assert status in (0, 1)  # 0 : manual, 1 : auto
        conn = sqlite3.connect(self._dir)
        c = conn.cursor()

        c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')

        if c.fetchone() is None:
            c.execute(f'INSERT INTO chatroom values({chatId}, {status})')

        else:
            c.execute(f'UPDATE chatroom SET status={status} WHERE chatId={chatId}')

        conn.commit()
        conn.close()


    def setMode(self, chatId, mode):
        assert mode in ('auto', 'manual')
        status = 1 if mode == 'auto' else 0
        self._writeStatus(chatId, status)


    def isRegistered(self, chatId):
        status = self._readStatus(chatId)
        return status is not None


    def isAutoMode(self, chatId):
        status = self._readStatus(chatId)
        return status == 1




# db_dir = './database/channel.db'
#
#
# def read(chatId):
#     conn = sqlite3.connect(db_dir)
#     c = conn.cursor()
#
#     c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')
#     res = c.fetchone()
#
#     return res[0] if res is not None else None
#
#
# def write(chatId, mode):
#     assert mode in (0, 1)
#     conn = sqlite3.connect(db_dir)
#     c = conn.cursor()
#
#     c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')
#
#     if c.fetchone() is None:
#         c.execute(f'INSERT INTO chatroom values({chatId}, {mode})')
#
#     else:
#         c.execute(f'UPDATE chatroom SET status={mode} WHERE chatId={chatId}')
#
#     conn.commit()
#     conn.close()
#
#
# def activate(chatId):
#     write(chatId, 1)
#
#
# def deactivate(chatId):
#     write(chatId, 0)
#
# # delete activate, deactivate and replace with this
# def setMode(chatId, mode):
#     assert mode in ('auto', 'manual')
#     key = 1 if mode == 'auto' else 0
#     write(chatId, 0)
#
#
#
# def isRegistered(chat):
#     chatId = chat.chatId
#     status = read(chatId)
#     return status is not None
#
#
# def isActivated(chat):
#     chatId = chat.chatId
#     status = read(chatId)
#     return status == 1
