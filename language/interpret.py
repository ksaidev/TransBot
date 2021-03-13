import language.papago as translate_to
from language.wrapper import wrap
import DB.word_DB as WordDB
import re


def letterLang(letter):
    assert len(letter) == 1, 'input value must be a single letter'

    if ord('가') <= ord(letter) <= ord('힣'):
        return 2  # kor

    elif ord('ㄱ') <= ord(letter) <= ord('ㆌ'):
        return 0.2  # incomplete kor

    elif ord('a') <= ord(letter.lower()) <= ord('z'):
        return -1  # eng

    else:
        return 0  # none


def isKoreanString(input_s):
    cnt = 0
    for c in input_s:
        cnt += letterLang(c)

    return cnt >= 0



def interpreter(string):
    if isKoreanString(string):
        data = WordDB.ko_en()
        for key in data:
            string = string.replace(key, data[key])

        return translate_to.eng(string)

    else:
        data = WordDB.en_ko()
        for key in data:
            string = str(re.sub(key, data[key], string, flags=re.IGNORECASE))

        wrapped_str, subst_dict = wrap(string)

        res = translate_to.kor(wrapped_str)

        for key in subst_dict:
            res = res.replace(key, subst_dict[key])

        return res


if __name__ == '__main__':
    print(interpreter(''''''))
