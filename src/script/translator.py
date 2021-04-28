from src.module.papago import PapagoAPI
# from src.script.will_be_deleted.wrapper import wrap
from src.data.word_db import WordDatabase
import re


class Translator:
    def __init__(self):
        self.api = PapagoAPI()
        pass

    def translate(self, text):
        if self._is_korean_text(text):
            pass

        else:
            pass


    @staticmethod
    def _is_korean_word(word):
        return re.search('[ㄱ-ㅎㅏ-ㅣ가-힣]', word) is not None

    @staticmethod
    def _is_korean_text(text):
        """
        Checks if the text is Korean or not
        Determined by comparing the number of words in each language
        """
        words = text.split()
        total = len(words)
        kor_count = 0

        for word in words:
            if Translator._is_korean_word(word):
                kor_count += 1

        return kor_count >= total // 2

    @staticmethod
    def _has_jong_seong(letter):
        """
        Returns if the letter has a jong seong
        Always return false if the input letter is not Korean
        """
        assert len(letter) == 1
        if Translator._is_korean_word(letter):
            return (ord(letter) - ord('가')) % 28 != 0
        return False

    @staticmethod
    def encode(text, word_table):
        """
        Encodes the custom words of TransBot so that it won't be translated by the Papago API
        The encode format is '%(number)('n' or 'p')%' (depending on the Jong Seong of the target word
        Returns the encoded text and the temporary lookup table for decoding
        """
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
            trailer = 'n' if Translator._has_jong_seong(target[-1]) else 'p'
            key = f'%{next(key_number)}{trailer}%'
            temp_lookup[key] = target
            return key

        return regex.sub(encoder, text), temp_lookup

    @staticmethod
    def decode(text, lookup_table):
        pass

    def link_protector(self):
        pass





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

        return api.get_translated_text(string, 'en')

    else:
        data = WordDB.en_ko()
        for key in data:
            string = str(re.sub(key, data[key], string, flags=re.IGNORECASE))

        wrapped_str, subst_dict = wrap(string)

        res = api.get_translated_text(string, 'ko')

        for key in subst_dict:
            res = res.replace(key, subst_dict[key])

        return res


if __name__ == '__main__':
    print(interpreter(''''''))
