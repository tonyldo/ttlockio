import requests
import time
from .constants import *

class TTlockAPIError(Exception):
    def __init__(self,error_code=-3,menssage='Invalid Parameter'):
        self.error_code = error_code
        self.menssage=menssage
    def __str__(self):
        return 'Error returned from TTlockAPI: Error_code {} - {}'.format(self.error_code,self.menssage)

class TTLock():
    def __init__(self, clientId=None,accessToken=None):
        self.clientId = clientId
        self.accessToken = accessToken
    
    def generate_gateways(self,pageSize=20):
        pageNo = 1
        totalPages = 1
        while self.__verify_page__(pageNo, totalPages):
            _url_request = GATEWAY_LIST_URL.format(
                API_URI,
                GATEWAY_LIST_RESOURCE,
                self.clientId,
                self.accessToken,
                pageNo,
                pageSize,
                self.__get_current_millis__(),
            )
            _response = self.__send_request__(_url_request).json()
            yield _response.get(LIST_FIELD)
            totalPages = _response.get(PAGES_FIELD)
            pageNo=pageNo+1

    @classmethod
    def __verify_page__(cls,pageNo, totalPages):
        return pageNo<=totalPages

    def __get_current_millis__(self):
        return int(round(time.time() * 1000))

    def locks_gateway_list(self,gatewayId=None):
        if not gatewayId:
            raise TTlockAPIError()

        _url_request = LOCKS_PER_GATEWAY_URL.format(
            API_URI,
            LOCKS_PER_GATEWAY_RESOURCE,
            self.clientId,
            self.accessToken,
            gatewayId,
            self.__get_current_millis__(),
        )
        return self.__send_request__(_url_request).json().get(LIST_FIELD)

    def generate_lock_records(self,lockId=None,pageSize=20,startDate=0,endDate=0):
        if not lockId:
            raise TTlockAPIError()

        pageNo = 1
        totalPages = 1
        while self.__verify_page__(pageNo, totalPages):
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
                self.__get_current_millis__(),
            )
            _response = self.__send_request__(_url_request).json()
            yield _response.get(LIST_FIELD)
            totalPages = _response.get(PAGES_FIELD)
            pageNo=pageNo+1
    
    def lock_state(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()
        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_STATE_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            self.__get_current_millis__(),
        )
        return self.__send_request__(_url_request).json().get(STATE_FIELD)

    def lock_electric_quantity(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()
        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_ELECTRIC_QUANTITY_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            self.__get_current_millis__(),
        )
        return self.__send_request__(_url_request).json().get(ELECTRIC_QUANTITY_FIELD)
    
    def __send_request__(self, _url_request):
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request('GET',_url_request, headers=_headers)
        if _response.status_code not in GOOD_HTTP_CODES:
            raise requests.HTTPError(_response.status_code)
        elif _response.json().get(ERROR_CODE_FIELD) :
            raise TTlockAPIError(error_code=_response.json().get(ERROR_CODE_FIELD),menssage=_response.json().get(MENSSAGE_FIELD))

        return _response