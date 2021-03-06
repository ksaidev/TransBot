from src.module.google_spread import GoogleSpread
# from src.module.preprocessor import PreProcessor
from src.module.replacer import Replacer
from data.private import GSPREAD_URL
import json
import threading


class WordDatabase:
    def __init__(self, db_dir='data/words.json'):
        self.dir = db_dir
        self.remote = self.Remote()
        self.load()

    def load(self):
        try:
            with open(self.dir, 'r') as f:
                data = json.load(f)
            Replacer.set_keyword_data(data)
        except json.decoder.JSONDecodeError:
            pass

    def save(self):
        data = Replacer.get_keyword_data()
        with open(self.dir, 'w') as f:
            json.dump(data, f, indent=None)

    def pull(self):
        """
        saves the data from the remote to the local
        returns error row data
        """
        remote_data, error_data = self.remote.get_data()

        for target in remote_data:
            for pair in remote_data[target].items():
                Replacer.add_keyword(pair, target)

        self.save()
        return error_data


    class Remote:
        """
        An inner class for handling google spreadsheet word database
        """
        def __init__(self, key_dir='data/remote_db_key.json', url=GSPREAD_URL):
            self.spread = GoogleSpread(key_dir, url)
            self.HEADER_HEIGHT = 2

        def get_data(self):
            """
            gets keyword data and error row data from google spreadsheet
            marks rows with errors on the spreadsheet
            """
            data = {
                'en': {}, 'ko': {}
            }
            error_data = {
                'ksa_words': {}, 'target_en': {}, 'target_ko': {}
            }

            # Get data from sheet 'ksa_words'
            # target_sheet = {}
            # ksa_words, target_sheet['ko'], target_sheet['en'] = self.spread.get_data()
            ksa_words = self.spread.get_data('ksa_words')

            # TODO : Optimize
            for row in range(len(ksa_words)):
                error = None
                to_append = {'ko': {}, 'en': {}}

                ko, en, sub_ko, sub_en = [word.strip() for word in ksa_words[row]]
                pair = {'ko': ko, 'en': en}
                sub_pair = {'ko': sub_ko, 'en': sub_en}

                for source, target in (('ko', 'en'), ('en', 'ko')):
                    target_word = pair[target]
                    source_word = pair[source]
                    if source_word == '' or source_word in data[target]:
                        error = source_word
                        break
                    to_append[target].update({source_word: target_word})

                    source_words = [word.strip() for word in sub_pair[source].split(',')]
                    if '' not in source_words:
                        pairs = {}
                        for source_word in source_words:
                            if source_word in data[target]:
                                error = source_word
                                break
                            pairs.update({source_word: target_word})
                        if not error:
                            to_append[target].update(pairs)
                if error is not None:
                    error_data['ksa_words'][row + self.HEADER_HEIGHT] = error
                else:
                    for target in ('ko', 'en'):
                        data[target].update(to_append[target])

            # Get data from sheet 'general(ko???en)', 'general(en???ko)'
            for target in ('ko', 'en'):
                table_name = f'target_{target}'
                # sheet = target_sheet[target]
                sheet = self.spread.get_data(table_name)

                for row in range(len(sheet)):
                    line = [word.strip() for word in sheet[row]]
                    if '' in line:
                        error_data[table_name][row + self.HEADER_HEIGHT] = ''
                        continue
                    source_word, target_word = line
                    if source_word in data[target]:
                        error_data[table_name][row + self.HEADER_HEIGHT] = source_word
                        continue
                    data[target].update({source_word: target_word})
            # Marking rows with errors on the sheet
            self.mark_error(error_data)
            return data, error_data


        def mark_error(self, error_rows):
            def mark_error_in_sheet(key):
                self.spread.color_reset(key)
                self.spread.color_rows(key, error_rows[key])
            for sheet_key in error_rows:
                thread = threading.Thread(target=mark_error_in_sheet, args=(sheet_key, ))
                thread.start()


    @staticmethod
    def has_jongseong(letter):
        order = ord(letter)
        if ord('???') <= order <= ord('???') or ord('???') <= order <= ord('???'):
            return (ord(letter) - ord('???')) % 28 != 0
        else:
            return False


if __name__ == '__main__':
    # local testing
    # db = WordDatabase(dir='words.db')
    # print(db.get_word_data('en'))

    from pprint import pprint
    # # remote testing
    print('start')
    db = WordDatabase.Remote(key_dir='C:/Python projects/TransBot/data/remote_db_key.json')
    print('init complete')
    data_, error_data_ = db.get_data()
    # pprint(data_)
    pprint(error_data_)

    # db = WordDatabase()
    # db.pull()
    # from pprint import pprint
    # pprint(data_)

