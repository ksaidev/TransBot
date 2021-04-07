import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import threading
import DB.word_DB as localDB
import private


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = './DB/transbot-worddb-key.json'
# json_file_name = 'transbot-worddb-key.json' # for local testing

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)
gc = gspread.authorize(credentials)


spreadsheet_url = private.gspread_url

doc = gc.open_by_url(spreadsheet_url)


sheets = dict()
sheets['ksa_words'] = doc.worksheet('ksa_words')
sheets['ko_en'] = doc.worksheet('general(ko→en)')
sheets['en_ko'] = doc.worksheet('general(en→ko)')


def colorRow(sheet, row, color):
    if color == 'red':
        rgb = {"red": 1, "green": 0.9, "blue": 0.9}
    elif color == 'yellow':
        rgb = {"red": 1, "green": 1, "blue": 0.8}
    else:
        rgb = {"red": 1, "green": 1, "blue": 1}

    sheet.format(f'A{row}:D{row}', {"backgroundColor": rgb})


def colorAllWhite(sheet, total):
    sheet.format(f'A2:D{total + 1}',
                 {"backgroundColor": {"red": 1, "green": 1, "blue": 1}})


def sync():
    errors = dict()
    total = 0
    for sheet_name in sheets:
        sheet = sheets[sheet_name]
        onlineDB = sheet.get_all_values()[1:]

        localDB.deleteAll(sheet_name)

        sheet_total = len(onlineDB)
        colorAllWhite(sheet, sheet_total)

        minor, major = localDB.write_rows(sheet_name, onlineDB)

        for row in minor:
            colorRow(sheet, row, 'yellow')

        for row in major:
            colorRow(sheet, row, 'red')

        errors[sheet_name] = [minor, major]
        total += sheet_total

    return errors, total


if __name__ == '__main__':
    print(sheets['ksa_words'].get_all_values())
