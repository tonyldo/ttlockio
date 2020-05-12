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
    
    def get_gateway_generator(self,pageSize=20):
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
            for gateway in _response.get(LIST_FIELD):
                yield gateway
            totalPages = _response.get(PAGES_FIELD)
            pageNo=pageNo+1

    @classmethod
    def __verify_page__(cls,pageNo, totalPages):
        return pageNo<=totalPages

    def __get_current_millis__(self):
        return int(round(time.time() * 1000))

    def get_locks_per_gateway_generator(self,gatewayId=None):
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
        
        for lock in self.__send_request__(_url_request).json().get(LIST_FIELD):
            yield lock

    def get_lock_records_generator(self,lockId=None,pageSize=20,startDate=0,endDate=0):
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
            for records in _response.get(LIST_FIELD):
                yield records
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
    
    def lock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()

        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            self.__get_current_millis__(),
        )
        return self.__is_erro_code_success__(self.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))

    def unlock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()

        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            UNLOCK_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            self.__get_current_millis__(),
        )
        return self.__is_erro_code_success__(self.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))


    def __is_erro_code_success__(self,erroCode=None):
        if not erroCode and erroCode==0:
            return True
        else:
            return False

    def __send_request__(self, _url_request):
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request('GET',_url_request, headers=_headers)
        if _response.status_code not in GOOD_HTTP_CODES:
            raise requests.HTTPError(_response.status_code)
        elif _response.json().get(ERROR_CODE_FIELD) :
            raise TTlockAPIError(error_code=_response.json().get(ERROR_CODE_FIELD),menssage=_response.json().get(MENSSAGE_FIELD))

        return _response