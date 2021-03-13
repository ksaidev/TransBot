import sqlite3

db_dir = './DB/chatroom_list.db'

def read(chatId):
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')
    res = c.fetchone()

    if res is None:
        return None

    else:
        return res[0]


def write(chatId, mode):
    assert mode in (0, 1)
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    c.execute(f'SELECT status FROM chatroom WHERE chatId={chatId}')

    if c.fetchone() is None:
        c.execute(f'INSERT INTO chatroom values({chatId}, {mode})')

    else:
        c.execute(f'UPDATE chatroom SET status={mode} WHERE chatId={chatId}')

    conn.commit()
    conn.close()

def activate(chatId):
    write(chatId, 1)

def deactivate(chatId):
    write(chatId, 0)

def isRegistered(chat):
    chatId = chat.chatId
    status = read(chatId)
    return status is not None

def isActivated(chat):
    chatId = chat.chatId
    status = read(chatId)
    return status == 1




