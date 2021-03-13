from translate import Translator


en_ko = Translator(from_lang='en', to_lang='ko')
ko_en = Translator(from_lang='ko', to_lang='en')


def kor(string):
    return en_ko.translate(string)

def eng(string):
    return ko_en.translate(string)


if __name__ == '__main__':
    print(kor('hello'))
