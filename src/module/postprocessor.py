import re

test = '아무말 아무말은 $4는 너무 비싸요. 이 $32n$을 $13p$했다. '
table = [''] * 33

table[32] = '사과'
table[13] = '바나나'



# s = test.split('$')
#
# for i in range(len(s)):
#     try:
#         index = int(s[i][:-1])
#         s[i] = table[index]
#     except (IndexError, ValueError):
#         pass
#
# print(''.join(s))

# for letter in test:
#     'p, n'

# p = re.compile(r'\$\d*[n|p]\$')
# print(p.findall(test))


def postprocess(text):
    regex = re.compile(r'\$\d*[n|p]\$')

    def encoder(mo):
        source = mo.string[mo.start():mo.end()]

        try:
            index = int(source[1:-2])
            return table[index]
        except (IndexError, ValueError):
            return source

    return regex.sub(encoder, text)

#
# def encode(word_table, text):
#     # Create a regular expression  from the dictionary keys
#     regex = re.compile("(%s)" % "|".join(map(re.escape, word_table.keys())), flags=re.I)
#
#     temp_lookup = {}
#
#     def key_generator():
#         key_num = 1
#         while True:
#             yield key_num
#             key_num += 1
#     key_number = key_generator()
#
#     def encoder(mo):
#         source = mo.string[mo.start():mo.end()].lower()
#         target = word_table[source]
#
#         key = f'${next(key_number)}$'
#         temp_lookup[key] = target
#         return key
#
#     return regex.sub(encoder, text), temp_lookup


if __name__ == "__main__":
    print(postprocess(test))

