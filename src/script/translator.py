from src.module.papago import PapagoAPI
from src.module.replacer import Replacer
import re


class Translator:
    def __init__(self):
        self.api = PapagoAPI()
        self.replacer = Replacer()

    def translate(self, text):
        target = 'en' if self._is_korean_text(text) else 'ko'

        preprocessed_text = self.replacer.preprocess(text, target)
        print(preprocessed_text)
        translated_text = self.api.get_translated_text(preprocessed_text, target)
        print(translated_text)
        postprocessed_text = self.replacer.postprocess(translated_text, target)

        return postprocessed_text


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


    def link_protector(self):
        pass


if __name__ == '__main__':
    tr = Translator()
    print(tr.translate('KSA is a school'))
