from data import private
import requests

class PapagoAPI:
    _keys = private.papago_keys
    _keyNumber = len(_keys)

    def __init__(self):
        self._idSeq = 0
        self._clientId, self._clientSecret = PapagoAPI._keys[self._idSeq]

    def getTranslatedText(self, text, target):
        assert target in ['ko', 'en']

        for _ in range(PapagoAPI._keyNumber):
            result = self._apiRequest(text, target)
            if result is not None:
                return result
            self._switchId()

        raise Exception('API limit exceeded')


    def _apiRequest(self, text, target):
        source = 'ko' if target == 'en' else 'en'

        request_url = 'https://openapi.naver.com/v1/papago/n2mt'
        headers = {'X-Naver-Client-Id': self._clientId,
                   'X-Naver-Client-Secret': self._clientSecret}
        params = {'source': source, 'target': target, 'text': text}
        try:
            response = requests.post(request_url, headers=headers, data=params)

            if response.status_code == 200:
                result = response.json()
                return result['message']['result']['translatedText']

            else:
                raise Exception('Papago API error')

        except requests.HTTPError:
            return None


    def _switchId(self):
        self._idSeq += 1
        self._idSeq %= PapagoAPI._keyNumber
        self._clientId, self._clientSecret = PapagoAPI._keys[self._idSeq]


if __name__ == '__main__':
    t = PapagoAPI()

    print(t.getTranslatedText('안녕', 'en'))
