def isKorLetter(letter):
    order = ord(letter.lower())
    return ord('가') <= order <= ord('힣') or ord('ㄱ') <= order <= ord('ㆌ')

def isDoubleWord(letter):
    return (ord(letter) - ord('가')) % 28 == 0

def wrap(string):
    string += 'a'
    res_str = ''
    prev = 'a'
    prevIsKor = False
    index = 0
    key = ''
    replacement = dict()

    for letter in string:
        isKor = isKorLetter(letter)

        if prevIsKor and not isKor:
            if isDoubleWord(prev):
                rep = f'${index}p$'
            else:
                rep = f'${index}n$'

            res_str += rep
            replacement[rep] = key

            index += 1
            key = ''

        if isKor:
            key += letter
        else:
            res_str += letter

        prev = letter
        prevIsKor = isKor

    res_str = res_str[:-1]
    return res_str, replacement
