from kakaoPy import client
from src.data import channel_db
from data import private

temp_disabled = []


class MyClass(client.Client):
    async def onMessage(self, chat):
        if chat.type in [1, 26]:
            message = chat.message

            if message[0] == '/':
                await chat.sendText(notice)

            else:
                chatId = chat.chatId
                if chatId not in temp_disabled:
                    if channel_db.isActivated(chat) or not channel_db.isRegistered(chat):
                        await chat.sendText(notice)
                        temp_disabled.append(chat.chatId)


def noticeMsg(input_str):
    if input_str == 'temp':
        return '임시 점검 중입니다. 잠시만 기다려 주세요.\n' \
               'Temporary maintenance in progress. Will be available shortly.'

    if input_str == 'emerg':
        return '서버 오류로 긴급 점검 중입니다. 잠시만 기다려 주세요.\n' \
               'Emergency maintenance in progress due to server error. Please wait a moment.'

    if input_str == 'update':
        return '서버 점검 및 업데이트 중입니다. 잠시만 기다려 주세요.\n' \
               'Server maintenance/update in progress. Will be available shortly.'

    return None


if __name__ == '__main__':
    print('Maintenance server console\nInput maintenance type (temp, emerg, update)')
    while True:
        console_input = input('> ')
        notice = noticeMsg(console_input)

        if notice is not None:
            break

        print('invalid command')

    print('Maintenance server start')

    client = MyClass("TransBot")
    client.run(private.kakao_id, private.kakao_pw)
