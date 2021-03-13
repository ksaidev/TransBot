from DB.database_sync import sync
import private

ADMIN_ROOMS = private.admin_rooms

major_errorlog = lambda sheet_name, major: f'Major error at sheet {sheet_name} row {str(major)[1:-1]}\n'
minor_errorlog = lambda sheet_name, minor: f'Minor error at sheet {sheet_name} row {str(minor)[1:-1]}\n'

sync_start = '동기화 중...\nSynchronizing...'
sync_complete = lambda total, errors: f'동기화 완료\nSync complete\nwritten : {total - errors}\nerrors : {errors}\ntotal : {total}'


def isAdminRoom(chatId):
    return chatId in ADMIN_ROOMS

def syncStart(chat):
    chatId = chat.chatId
    message = chat.message
    return isAdminRoom(chatId) and (message in ['/sync', '/동기화'])


def sync_log():
    logs = []
    errors, total = sync()
    error_num = 0

    for sheet_name in errors:
        minor, major = errors[sheet_name]

        if major:
            logs.append(major_errorlog(sheet_name, major))
        if minor:
            logs.append(minor_errorlog(sheet_name, minor))

        error_num += len(major) + len(minor)

    logs.append(sync_complete(total, error_num))

    return logs


'''
qwer = lambda major: f'Major error at row {str(major)[1:-1]}\n: overlapping words - try using synonym columns instead'


if message in ['/sync', '/동기화'] and chatId in [300090628526502, 238173194189938]:  # admin room code
    await chat.sendText('동기화 중...\nSynchronizing...')
    minor, major, total = sync()

    errors = len(minor) + len(major)
    if len(major) > 0:
        await chat.sendText(
            f'Major error at row {str(major)[1:-1]}\n: overlapping words - try using synonym columns instead')

    if len(minor) > 0:
        await chat.sendText(f'Minor error at row {str(minor)[1:-1]}\n: empty rows')

    await chat.sendText(f'동기화 완료\nSync complete\nwritten : {total - errors}\nerrors : {errors}\ntotal : {total}')'''