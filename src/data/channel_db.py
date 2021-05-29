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
        res = self.fetch()
        return res[0][0] if res != [] else None

    @Database.connection
    def set_mode(self, chat_id, status):
        assert status in (Mode.AUTO, Mode.MANUAL)
        self.execute(
            f'UPDATE chatroom SET status={status} WHERE chatId={chat_id}'
        )


if __name__ == '__main__':
    db = ChannelDatabase('../../data/channel.db')
    print(db.get_mode(166848140054575))
