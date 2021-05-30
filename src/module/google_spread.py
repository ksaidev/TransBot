import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio


class GoogleSpread:
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    SHEET_NAME = {
        'ksa_words': 'ksa_words',
        'target_ko': 'general(en→ko)',
        'target_en': 'general(en→ko)'
    }

    def __init__(self, key_dir, spreadsheet_url):
        self.key_dir = key_dir
        self.spreadsheet_url = spreadsheet_url
        self.sheet = {}
        self._sheet_init()

    def _sheet_init(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.key_dir, self.SCOPE
        )
        gc = gspread.authorize(credentials)
        doc = gc.open_by_url(self.spreadsheet_url)

        for sheet_key in self.SHEET_NAME:
            self.sheet[sheet_key] = doc.worksheet(self.SHEET_NAME[sheet_key])

    def get_data(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(asyncio.gather(
            *[self.get_data_sheet(sheet_key) for sheet_key in self.SHEET_NAME]
        ))

    async def get_data_sheet(self, sheet_key):
        return self.sheet[sheet_key].get_all_values()[1:]

    def color_rows(self, sheet_key, rows):
        color = {"red": 1, "green": 0.9, "blue": 0.9}
        for row in rows:
            self.sheet[sheet_key].format(
                f'A{row}:D{row}', {'backgroundColor': color}
            )

    def color_reset(self, sheet_key):
        self.sheet[sheet_key].format(
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
