import re


def encode(word_table, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, word_table.keys())), flags=re.I)

    temp_lookup = {}

    def key_generator():
        key_num = 1
        while True:
            yield key_num
            key_num += 1
    key_number = key_generator()

    def encoder(mo):
        source = mo.string[mo.start():mo.end()].lower()
        target = word_table[source]

        key = f'${next(key_number)}$'
        temp_lookup[key] = target
        return key

    return regex.sub(encoder, text), temp_lookup


if __name__ == "__main__":

    table = {
        '크사랑': 'ksarang',
        'ksa': '크사'
    }

    print(encode(table, "KSA is good"))
