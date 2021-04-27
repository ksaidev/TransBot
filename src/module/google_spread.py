import gspread
from oauth2client.service_account import ServiceAccountCredentials



class GoogleSpread:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]

    def __init__(self, key_dir, spreadsheet_url):
        self.key_dir = key_dir
        self.spreadsheet_url = spreadsheet_url


    def _get_sheet(self, sheet_key):
        assert sheet_key in ('ksa_words', 'target_ko', 'target_en')
        sheet_name = 'general(ko→en)' if sheet_key == 'target_en' else \
                     'general(en→ko)' if sheet_key == 'target_ko' else \
                     'ksa_words'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.key_dir, self.scope
        )
        gc = gspread.authorize(credentials)
        doc = gc.open_by_url(self.spreadsheet_url)

        return doc.worksheet(sheet_name)

    def get_data(self, sheet_key):
        sheet = self._get_sheet(sheet_key)
        return sheet.get_all_values()[1:]

    def color_rows(self, sheet_key, rows):
        sheet = self._get_sheet(sheet_key)
        color = {"red": 1, "green": 0.9, "blue": 0.9}
        for row in rows:
            sheet.format(
                f'A{row}:D{row}', {'backgroundColor': color}
            )

    def color_reset(self, sheet_key):
        sheet = self._get_sheet(sheet_key)
        sheet.format(
            f'A2:D',
            {"backgroundColor": {"red": 1, "green": 1, "blue": 1}}
        )




if __name__ == '__main__':
    # Local testing
    from data.private import GSPREAD_URL

    key_directory = 'C:/Python projects/TransBot/data/remote_db_key.json'

    g = GoogleSpread(key_directory, GSPREAD_URL)
    # print(g.get_data())
    # [['갠톡', 'personal chat'], ['단톡', 'group chat']]
    # g.color_reset()
    # for row in range(2, 20, 2):
    #     g.sheet.format(
    #         f'A{row}:B{row}',
    #         {'backgroundColor': {"red": 1, "green": 0.9, "blue": 0.9}}
    #     )
    red = {'backgroundColor': {"red": 1, "green": 0.9, "blue": 0.9}}
    # g.sheet.format(
    #     ['A2:B2', 'A4:B4'], red
    # )
