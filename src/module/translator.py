from src.module.papago import PapagoAPI
from src.module.replacer import Replacer
from src.bot.exceptions import KeywordTranslationError
import re


class Translator:
    def __init__(self):
        self.api = PapagoAPI()

    def translate(self, text):
        target = 'en' if self._is_korean_text(text) else 'ko'

        for _ in range(3):
            try:
                replacer = Replacer(target)
                preprocessed_text = replacer.preprocess(text)
                translated_text = self.api.get_translated_text(preprocessed_text, target)
                postprocessed_text = replacer.postprocess(translated_text)
            except IndexError:
                pass
            else:
                return postprocessed_text
        raise KeywordTranslationError


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
        kor_count = 0
        eng_count = 0

        for word in words:
            if Translator._is_korean_word(word):
                kor_count += 1
            else:
                eng_count += 1

        return kor_count >= eng_count


if __name__ == '__main__':
    tr = Translator()
    print(tr.translate('한과영은 좋은 학교에요'))
