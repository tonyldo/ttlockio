import requests
from .constants import *
from datetime import datetime

class TTlockAPIError(Exception):
    def __init_(self,error_code=-3,menssage='Invalid Parameter'):
        self.error_code = error_code
        self.menssage=menssage
    def __str__(self):
        return 'Error returned from TTlockAPI: Error_code {} - {}'.format(self.error_code,self.menssage)

class TTLock():
    def __init__(self, clientId,accessToken):
        self.clientId = clientId
        self.accessToken = accessToken

    def gateways_list(self,pageNo=1,pageSize=20):
        _url_request = GATEWAY_LIST_URL.format(
            API_URI,
            GATEWAY_LIST_RESOURCE,
            self.clientId,
            self.accessToken,
            pageNo,
            pageSize,
            datetime.timestamp(datetime.now()),
        )
        _response = self.send_request(_url_request).json()

        if len(_response.get(LIST_FIELD)) == 0:
            return _response.get(LIST_FIELD) 
        else:
            return _response.get(LIST_FIELD)  + self.gateways_list(pageNo=pageNo + 1,pageSize=pageSize)

    def locks_gateway_list(self,gatewayId=None):
        if not gatewayId:
            raise TTlockAPIError()

        _url_request = LOCKS_PER_GATEWAY_URL.format(
            API_URI,
            LOCKS_PER_GATEWAY_RESOURCE,
            self.clientId,
            self.accessToken,
            gatewayId,
            datetime.timestamp(datetime.now()),
        )
        return self.send_request(_url_request).json().get(LIST_FIELD)
    
    def lock_records_list(self,lockId=None,pageNo=1,pageSize=20,startDate=0,endDate=0):
        if not lockId:
            raise TTlockAPIError()

        _url_request = LOCK_RECORDS_URL.format(
            API_URI,
            LOCK_RECORDS_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            pageNo,
            pageSize,
            startDate,
            endDate,
            datetime.timestamp(datetime.now()),
        )
        _response = self.send_request(_url_request).json()

        if len(_response.get(LIST_FIELD)) == 0:
            return _response.get(LIST_FIELD) 
        else:
            return _response.get(LIST_FIELD)  + self.lock_records_list(lockId,pageNo=pageNo + 1,pageSize=pageSize,startDate=startDate,endDate=endDate)

    def lock_state(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()
        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_STATE_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            datetime.timestamp(datetime.now()),
        )
        return self.send_request(_url_request).json().get(STATE_FIELD)

    def lock_electric_quantity(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()
        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_ELECTRIC_QUANTITY_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            datetime.timestamp(datetime.now()),
        )
        return self.send_request(_url_request).json().get(ELECTRIC_QUANTITY_FIELD)
    
    def send_request(self, _url_request):
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request('GET',_url_request, headers=_headers)
        if _response.status_code not in GOOD_HTTP_CODES:
            raise requests.HTTPError(_response.status_code)
        elif _response.json().get(ERROR_CODE_FIELD) :
            raise TTlockAPIError(_response.json().get(ERROR_CODE_FIELD),_response.json().get(MENSSAGE_FIELD))

        return _response