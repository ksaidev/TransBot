import requests
from data.private import PAPAGO_KEYS
from src.script.exceptions import ApiLimitExceeded, UndefinedError


class PapagoAPI:
    _keys = PAPAGO_KEYS
    _key_number = len(_keys)

    def __init__(self):
        self._current_id_num = 0
        self._CLIENT_ID, self._CLIENT_SECRET = PapagoAPI._keys[self._current_id_num]

    def get_translated_text(self, text, target):
        assert target in ['ko', 'en']

        for _ in range(PapagoAPI._key_number):
            result = self._api_request(text, target)
            if result is not None:
                return result
            self._switch_id()

        raise ApiLimitExceeded


    def _api_request(self, text, target):
        source = 'ko' if target == 'en' else 'en'

        request_url = 'https://openapi.naver.com/v1/papago/n2mt'
        headers = {'X-Naver-Client-Id': self._CLIENT_ID,
                   'X-Naver-Client-Secret': self._CLIENT_SECRET}
        params = {'source': source, 'target': target, 'text': text}
        try:
            response = requests.post(request_url, headers=headers, data=params)

            if response.status_code == 200:
                result = response.json()
                return result['message']['result']['translatedText']

            else:
                raise UndefinedError

        except requests.HTTPError:
            return None


    def _switch_id(self):
        self._current_id_num += 1
        self._current_id_num %= PapagoAPI._key_number
        self._CLIENT_ID, self._CLIENT_SECRET = PapagoAPI._keys[self._current_id_num]


if __name__ == '__main__':
    t = PapagoAPI()

    print(t.get_translated_text('$1s$ is good', 'ko'))
