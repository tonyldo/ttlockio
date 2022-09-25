import argparse
import requests
import hashlib
import time
from .constants import *

class TTlockAPIError(Exception):
    def __init__(self,error_code=-3,menssage='Invalid Parameter'):
        self.error_code = error_code
        self.menssage=menssage
    def __str__(self):
        return 'Error returned from TTlockAPI: Error_code {} - {}'.format(self.error_code,self.menssage)

class TTLock():

    @classmethod
    def __is_erro_code_success__(cls,erroCode=None):
        if not erroCode and erroCode==0:
            return True
        else:
            return False

    @classmethod
    def __send_request__(cls, _url_request,method='GET'):
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request(method,_url_request, headers=_headers)
        _response.raise_for_status()
        if _response.json().get(ERROR_CODE_FIELD) :
            raise TTlockAPIError(error_code=_response.json().get(ERROR_CODE_FIELD),menssage=_response.json().get(MENSSAGE_FIELD))

        return _response


    def create_user_script_entry():
        parser = argparse.ArgumentParser(description='Create TTLock User.')
        parser.add_argument('clientId', metavar='clientId', help='TTLock Client Id')
        parser.add_argument('clientSecret', metavar='clientSecret', help='TTLock Client Secret')
        parser.add_argument('username', metavar='username', help='Your new users username')
        parser.add_argument('password', metavar='password', help='Your new users password')
        parser.add_argument('--redirect_url', help='Rediect URL for your application', required=False, default="")   
        
        parser.add_argument('--token', action='store_const', const=1, help='Generate Access Token')
        
        args = parser.parse_args()
        result = TTLock.create_user(args.clientId,args.clientSecret,args.username,args.password)
        print(result)

        if args.token:
            print(TTLock.get_token(args.clientId,args.clientSecret,result["username"],args.password,args.redirect_url))


    def refresh_token_script_entry():
        parser = argparse.ArgumentParser(description='Refresh TTLock Access Token.')
        parser.add_argument('clientId', metavar='clientId', help='TTLock Client Id')
        parser.add_argument('clientSecret', metavar='clientSecret', help='TTLock Client Secret')
        parser.add_argument('refresh', metavar='refresh', help='Your refresh token')
        parser.add_argument('--redirect_url', help='Rediect URL for your application', required=False, default="")   
                
        args = parser.parse_args()
        result = TTLock.refresh_token(args.clientId,args.clientSecret,args.refresh,args.redirect_url)
        print(result)
        

    @classmethod
    def create_user(cls,clientId,clientSecret,username,password):
        if (not password.islower()) or len(password)>32 or len(username)==0 or username.strip()=='':
            raise TTlockAPIError()

        _url_request = USER_CREATE_URL.format(
            API_URI,
            USER_RESOURCE,
            clientId,
            clientSecret,
            username,
            hashlib.md5(password.encode()).hexdigest(),
            TTLock.__get_current_millis__(),
        )

        return TTLock.__send_request__(_url_request).json()


    @classmethod
    def get_token(cls,clientId,clientSecret,username,password,redirect_uri,hashed_password=False):
        if not hashed_password:
            password = hashlib.md5(password.encode()).hexdigest()
            
        _url_request = TOKEN_CREATE_URL.format(
            TOKEN_RESOURCE,
            clientId,
            clientSecret,
            username,
            password,
            redirect_uri,
        )

        return TTLock.__send_request__(_url_request,'POST').json()
    
    @classmethod
    def refresh_token(cls,clientId,clientSecret,refresh,redirect_uri):
        _url_request = TOKEN_REFRESH_URL.format(
            TOKEN_RESOURCE,
            clientId,
            clientSecret,
            refresh,
            redirect_uri,
        )

        return TTLock.__send_request__(_url_request,'POST').json()

    @classmethod
    def __verify_page__(cls,pageNo, totalPages):
        return pageNo<=totalPages
    
    @classmethod
    def __get_current_millis__(cls):
        return int(round(time.time() * 1000))

    def __init__(self, clientId=None,accessToken=None):
        self.clientId = clientId
        self.accessToken = accessToken
    
    def get_gateway_generator(self,pageSize=20):
        pageNo = 1
        totalPages = 1
        while TTLock.__verify_page__(pageNo, totalPages):
            _url_request = GATEWAY_LIST_URL.format(
                API_URI,
                GATEWAY_LIST_RESOURCE,
                self.clientId,
                self.accessToken,
                pageNo,
                pageSize,
                TTLock.__get_current_millis__(),
            )
            _response = TTLock.__send_request__(_url_request).json()
            for gateway in _response.get(LIST_FIELD):
                yield gateway
            totalPages = _response.get(PAGES_FIELD)
            pageNo=pageNo+1

    def get_locks_per_gateway_generator(self,gatewayId=None):
        if not gatewayId:
            raise TTlockAPIError()

        _url_request = LOCKS_PER_GATEWAY_URL.format(
            API_URI,
            LOCKS_PER_GATEWAY_RESOURCE,
            self.clientId,
            self.accessToken,
            gatewayId,
            TTLock.__get_current_millis__(),
        )
        
        for lock in TTLock.__send_request__(_url_request).json().get(LIST_FIELD):
            yield lock

    def get_lock_records_generator(self,lockId=None,pageSize=20,startDate=0,endDate=0):
        if not lockId:
            raise TTlockAPIError()

        pageNo = 1
        totalPages = 1
        while TTLock.__verify_page__(pageNo, totalPages):
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
                TTLock.__get_current_millis__(),
            )
            _response = TTLock.__send_request__(_url_request).json()
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
            TTLock.__get_current_millis__(),
        )
        return TTLock.__send_request__(_url_request).json().get(STATE_FIELD)

    def lock_electric_quantity(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()
        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_ELECTRIC_QUANTITY_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__send_request__(_url_request).json().get(ELECTRIC_QUANTITY_FIELD)
    
    def lock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()

        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            LOCK_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__is_erro_code_success__(TTLock.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))

    def unlock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError()

        _url_request = LOCK_QUERY_URL.format(
            API_URI,
            UNLOCK_RESOURCE,
            self.clientId,
            self.accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__is_erro_code_success__(TTLock.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))
