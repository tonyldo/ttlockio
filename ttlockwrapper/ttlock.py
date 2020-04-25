import requests
from datetime import datetime

GOOD_HTTP_CODES = [200, 201, 202, 203]
TOKEN_ERROR_CODES = [10003]
API_URI='https://api.ttlock.com/v3'
GATEWAY_LIST_RESOURCE = 'gateway/list'

ERROR_CODE_FIELD = 'errcode'

class TTLock():
    def __init__(self, clientId,accessToken):
        self.clientId = clientId
        self.accessToken = accessToken

    def gateways_list(self,pageNo=1,pageSize=20):
        _url_request = 'https://{}/{}?client_id={}&accessToken={}&pageNo={}&pageSize={}&date={}'.format(
            API_URI,
            GATEWAY_LIST_RESOURCE,
            self.clientId,
            self.accessToken,
            pageNo,
            pageSize,
            datetime.timestamp(datetime.now()),
        )
        _response = self.send_request(_url_request).json()

        if len(_response.get('list')) == 0:
            return _response.get('list') 
        else:
            return _response.get('list')  + self.gateways_list(pageNo=pageNo + 1,pageSize=pageSize)

    def send_request(self, _url_request):
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request('GET',_url_request, headers=_headers)
        if _response.status_code not in GOOD_HTTP_CODES:
            raise Exception('HTTP_ERROR', _response.status_code)
        elif _response.json().get(ERROR_CODE_FIELD) in TOKEN_ERROR_CODES:
            raise PermissionError('API_TOKEN_ERROR', _response.json().get(ERROR_CODE_FIELD))
        elif _response.json().get(ERROR_CODE_FIELD) :
            raise ValueError('API_ERROR', _response.json().get(ERROR_CODE_FIELD))

        return _response