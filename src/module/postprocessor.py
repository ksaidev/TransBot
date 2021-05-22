import re

class PostProccesor:
    def __init__(self):
        self.data = []

    def set_keyword_data(self, data):
        self.data = data

    def process(self, text):
        regex = re.compile(r'\$\d*[n|p]\$')

        def encoder(mo):
            source = mo.string[mo.start():mo.end()]
            try:
                index = int(source[1:-2])
                return self.data[index]
            except (IndexError, ValueError):
                return source

        return regex.sub(encoder, text)



if __name__ == "__main__":
    test = '아무말 아무말은 $4는 너무 비싸요. 이 $32n$을 $13p$했다. '
    table = [''] * 33

    table[32] = '사과'
    table[13] = '바나나'

    processor = PostProccesor()
    processor.set_keyword_data(table)
    print(processor.process(test))

