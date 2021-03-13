import sqlite3

db_dir = './DB/words.db'
#db_dir = 'words.db'  # for local testing

def write(sheet_name, pair):  # [kor, eng, sy_kor, sy_eng]
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    pair_str = str(pair)[1:-1]

    c.execute(f'INSERT INTO {sheet_name} values({pair_str})')

    conn.commit()
    conn.close()


def write_rows(sheet_name, pairs):
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    major = []
    minor = []
    row = 2

    for pair in pairs:
        pair_str = str(pair)[1:-1]

        if pair[0:2] == ['']*2:
            minor.append(row)

        elif '' in pair[0:2]:
            major.append(row)

        else:
            try:
                c.execute(f'INSERT INTO {sheet_name} values({pair_str})')

            except sqlite3.IntegrityError:
                major.append(row)

        row += 1

    conn.commit()
    conn.close()
    return minor, major


def read(sheet_name):
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    c.execute(f'SELECT * FROM {sheet_name}')
    res = c.fetchall()

    return res


def deleteAll(sheet_name):
    conn = sqlite3.connect(db_dir)
    c = conn.cursor()

    c.execute(f'DELETE FROM {sheet_name}')

    conn.commit()
    conn.close()


def ko_en():
    res = dict()

    # read KSA word DB
    for pair in read('ksa_words'):
        kor, eng, synonyms, _ = pair
        res[kor] = eng

        if synonyms != '':
            sy_list = synonyms.split(',')

            for key in sy_list:
                kor_synonym = key.strip()
                res[kor_synonym] = eng

    # read general(ko_en) DB
    for pair in read('ko_en'):
        kor, eng = pair
        res[kor] = eng

    return res


def en_ko():
    res = dict()

    # read KSA word DB
    for pair in read('ksa_words'):
        kor, eng, _, synonyms = pair
        res[eng.lower()] = kor

        if synonyms != '':
            sy_list = synonyms.split(',')

            for key in sy_list:
                eng_synonym = key.strip()
                res[eng_synonym.lower()] = kor

    # read general(en_ko) DB
    for pair in read('en_ko'):
        eng, kor = pair
        res[eng.lower()] = kor

    return res


if __name__ == '__main__':
    print(read('en_ko'))
