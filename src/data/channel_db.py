from src.data.database import Database
from src.constants.mode import Mode

class ChannelDatabase(Database):
    def __init__(self, dir='./data/channel.db'):
        super().__init__(dir)

    @Database.connection
    def add_channel(self, chat_id):
        status = Mode.AUTO
        self.execute(
            'INSERT INTO chatroom values (?, ?)', (chat_id, status)
        )

    @Database.connection
    def get_mode(self, chat_id):
        self.execute(
            f'SELECT status FROM chatroom WHERE chatId={chat_id}'
        )
        res = self.fetch()[0]
        return res[0] if res is not None else None

    @Database.connection
    def set_mode(self, chat_id, status):
        assert status in (Mode.AUTO, Mode.MANUAL)
        self.execute(
            f'UPDATE chatroom SET status={status} WHERE chatId={chat_id}'
        )



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