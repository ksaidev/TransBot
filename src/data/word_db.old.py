import sqlite3
from src.data.database import Database
from src.module.google_spread import GoogleSpread
from data.private import GSPREAD_URL


class WordDatabase(Database):
    def __init__(self, dir='../data/words.db'):
        super().__init__(dir)
        self.remote = self.Remote()

    def get_word_data(self, target):
        """
        Gets the source, target word pairs from 'target_(lang)' table in db
        Returns a encode={source: %keycode%}, decode={%keycode%: target} dict
        * uses a custom method using row_factory for accessing database
        """
        assert target in ('ko', 'en')


        _connection = sqlite3.connect(self._dir)


        self.execute(
            f'SELECT * FROM target_{target}'
        )
        word_data = self.fetch()
        return word_data


    # @Database.connection
    # def write_rows(self, target, data):
    #     pass


    def _reset(self, table_name):
        self.execute(
            f'DELETE from {table_name}'
        )

    def _insert(self, table_name, pair):
        self.execute(
            f'INSERT INTO {table_name} values (?, ?)', pair
        )

    # def _contains(self, ta, source_item):
    #     self.execute(
    #         f'SELECT FROM target_{target} WHERE source={source_item}'
    #     )
    #     return self.fetch() != []

    def _order(self, table_name):
        self.execute(
            f'SELECT * FROM {table_name} ORDER BY LENGTH source'
        )

    @Database.connection
    def pull(self):
        data, error_data = self.remote.get_data()

        for table_name in data:
            table = data[table_name]
            self._reset(table_name)
            for source_word in table:
                target_word = table[source_word]
                self._insert(table_name, (source_word, target_word))
            self._order(table_name)

        return error_data


    class Remote:
        def __init__(self, key_dir='../data/remote_db_key.json', url=GSPREAD_URL):
            self.spread = GoogleSpread(key_dir, url)
            self.HEADER_HEIGHT = 2

        def get_data(self):
            data = {
                'target_en': {}, 'target_ko': {}
            }
            error_data = {
                'ksa_words': {}, 'target_en': {}, 'target_ko': {}
            }

            # Get data from sheet 'ksa_words'
            ksa_words = self.spread.get_data('ksa_words')
            for row in range(len(ksa_words)):
                error = None
                to_append = {'ko': {}, 'en': {}}

                ko, en, sub_ko, sub_en = [word.strip() for word in ksa_words[row]]
                pair = {'ko': ko, 'en': en}
                sub_pair = {'ko': sub_ko, 'en': sub_en}

                for source, target in (('ko', 'en'), ('en', 'ko')):
                    target_word = pair[target]
                    source_word = pair[source]
                    if source_word == '' or source_word in data[f'target_{target}']:
                        error = source_word
                        break
                    to_append[target].update({source_word: target_word})

                    source_words = [word.strip() for word in sub_pair[source].split(',')]
                    if '' not in source_words:
                        pairs = {}
                        for source_word in source_words:
                            if source_word in data[f'target_{target}']:
                                error = source_word
                                break
                            pairs.update({source_word: target_word})
                        if not error:
                            to_append[target].update(pairs)
                if error is not None:
                    error_data['ksa_words'][row + self.HEADER_HEIGHT] = error
                else:
                    for target in ('ko', 'en'):
                        data[f'target_{target}'].update(to_append[target])

            # Get data from sheet 'general(ko→en)', 'general(en→ko)'
            for target in ('ko', 'en'):
                table_name = f'target_{target}'
                sheet = self.spread.get_data(table_name)

                for row in range(len(sheet)):
                    line = [word.strip() for word in sheet[row]]
                    if '' in line:
                        error_data[table_name][row + self.HEADER_HEIGHT] = ''
                        continue
                    source_word, target_word = line
                    if source_word in data[table_name]:
                        error_data[table_name][row + self.HEADER_HEIGHT] = source_word
                        continue

                    data[table_name].update({source_word: target_word})

            # Marking rows with errors on the sheet
            self.mark_error(error_data)
            return data, error_data


        def mark_error(self, error_rows):
            for sheet_key in error_rows:
                self.spread.color_rows(sheet_key, error_rows[sheet_key])


if __name__ == '__main__':
    # local testing
    # db = WordDatabase(dir='words.db')
    # print(db.get_word_data('en'))

    from pprint import pprint
    # remote testing
    db = WordDatabase.Remote(key_dir='C:/Python projects/TransBot/data/remote_db_key.json')
    data_, error_data_ = db.get_data()
    pprint(error_data_)

