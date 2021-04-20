from src.language.papago import PapagoAPI
from src.language.wrapper import wrap
import src.data.word_db as WordDB
import re

#TODO

class Translator:
    def __init__(self):
        self.api = PapagoAPI()
        pass

    def translate(self, text):
        if self._isKorean(text):
            pass

        else:
            pass


    def replaceKey(self):
        pass



    @staticmethod
    def _isKorean(text):
        letters = text.split()
        total = len(letters)
        korCount = 0

        for letter in letters:
            if re.search('[ㄱ-ㅎㅏ-ㅣ가-힣]', letter) is not None:
                korCount += 1

        return korCount >= total // 2





api = PapagoAPI()

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
    return sum(letterLang(c) for c in input_s) >= 0


def interpreter(string):
    if isKoreanString(string):
        data = WordDB.ko_en()
        for key in data:
            string = string.replace(key, data[key])

        return api.getTranslatedText(string, 'en')

    else:
        data = WordDB.en_ko()
        for key in data:
            string = str(re.sub(key, data[key], string, flags=re.IGNORECASE))

        wrapped_str, subst_dict = wrap(string)

        res = api.getTranslatedText(string, 'ko')

        for key in subst_dict:
            res = res.replace(key, subst_dict[key])

        return res


if __name__ == '__main__':
    print(interpreter(''''''))
