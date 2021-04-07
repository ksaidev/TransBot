import urllib.request
import json
import private

ID = private.papago_keys

id_num = 0
client_id, client_secret = ID[id_num]


def change_id():
    global id_num
    global client_id, client_secret

    id_num = (id_num+1) % len(ID)
    client_id, client_secret = ID[id_num]


def api_request(string, to_eng):
    encText = urllib.parse.quote(string)
    if to_eng:
        data = "source=ko&target=en&text=" + encText
    else:
        data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()

        res = json.loads(response_body.decode('utf-8'))
        return res['message']['result']['translatedText']

    else:
        return 'translate error'


def translate(string, to_eng):
    for _ in ID:
        try:
            translated_str = api_request(string, to_eng)
            return translated_str

        except Exception as e:
            change_id()

    return 'api key error'


def kor(string):
    return translate(string, False)


def eng(string):
    return translate(string, True)


def letterLang(letter):
    assert len(letter) == 1, 'input value must be a single letter'

    if ord('가') <= ord(letter) <= ord('힣'):
        return 'kor'

    elif ord('a') <= ord(letter.lower()) <= ord('z'):
        return 'eng'

    else:
        return None


def isKoreanString(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if letterLang(c) == 'kor':
            k_count += 1
        elif letterLang(c) == 'eng':
            e_count += 1

    return k_count >= e_count


async def trans(string):
    if isKoreanString(string):
        return eng(string)
    else:
        return kor(string)


if __name__ == '__main__':
    print(kor('hello 순호'))
