from DB.database_sync import sync
import private

ADMIN_ROOMS = private.admin_rooms


def major_errorlog(
    sheet_name, major): return f'Major error at sheet {sheet_name} row {str(major)[1:-1]}\n'


def minor_errorlog(
    sheet_name, minor): return f'Minor error at sheet {sheet_name} row {str(minor)[1:-1]}\n'


sync_start = '동기화 중...\nSynchronizing...'


def sync_complete(
    total, errors): return f'동기화 완료\nSync complete\nwritten : {total - errors}\nerrors : {errors}\ntotal : {total}'


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
