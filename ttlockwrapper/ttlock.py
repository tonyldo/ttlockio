import argparse
import requests
import hashlib
import time
import datetime
from .constants import *

class TTlockAPIError(Exception):
    def __init__(self,error_code=-3,message='Invalid Parameter'):
        self.error_code = error_code
        self.message=message
    def __str__(self):
        return 'Error returned from TTlockAPI: Error_code {} - {}'.format(self.error_code,self.message)

class TTLock():

    def _setAccessToken(self, accessToken=None):
        self._accessToken = accessToken
    def _getAccessToken(self):
        return self._accessToken

    def _setEndpoint(self, endpoint=EU_API_URI):
        self._endpoint = endpoint
    def _getEndpoint(self):
        return self._endpoint
    
    def _setClientId(self, clientId=None):
        self._clientId = clientId
    def _getClientId(self):
        return self._clientId
    
    accessToken = property(_getAccessToken, _setAccessToken)
    endpoint = property(_getEndpoint, _setEndpoint)
    clientId = property(_getClientId, _setClientId)

    def __init__(self, clientId, endpoint=EU_API_URI):
        self._clientId = clientId
        self._endpoint = endpoint
        self._accessToken = ""
    
    ## -------
    ## Helper methods
    ## -------

    @classmethod
    def __is_erro_code_success__(cls,erroCode=None):
        ## Is this an error? 
        if not erroCode and erroCode==0:
            return True
        else:
            return False

    @classmethod
    def __get_current_millis__(cls):
        # Get current time in milliseconds to define the expiration time.  
        return int(round(time.time() * 1000))

    @classmethod
    def __send_request__(cls, _url_request,method='GET'):
        ## Send an error, return a response or raise an exception.  
        _headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        _response = requests.request(method,_url_request, headers=_headers)
        _response.raise_for_status()
        if _response.json().get(ERROR_CODE_FIELD) :
            raise TTlockAPIError(error_code=_response.json().get(ERROR_CODE_FIELD),message=_response.json().get(MESSAGE_FIELD))

        return _response   

    @classmethod
    def __verify_page__(cls,pageNo, totalPages):
        return pageNo<=totalPages
    
    @classmethod
    def __get_expiry_millis__(cls, expiresIn):
        # Get current time in milliseconds to define the expiration time.  
        return TTLock.__get_current_millis__() + expiresIn
        
        
    def getExpiryMilliseconds(self, expiresIn):
        return TTLock.__get_expiry_millis__(expiresIn)
    
    def getExpiryDatetime(self, expiresIn):
        return datetime.datetime.fromtimestamp(TTLock.__get_expiry_millis__(expiresIn)/1000.0)
    ## -------
    ## End Helper methods
    ## -------
    
    ## -------
    ## OAuth2 Token methods
    ## -------
    
    def get_token(self,clientSecret,username,password,hashed_password=False):
        ## This method gets an access token, based on :
        ## clientSecret (from TTAPI website) - relevant to app on website (not the actual app)
        ## username - user's username
        ## password - user's password
        ## hashed_password - if the user's password is already MD5 hashed, pass in true
        
        if not hashed_password:
            password = hashlib.md5(password.encode()).hexdigest()
            
        _url_request = TOKEN_CREATE_URL.format(
            self._endpoint,
            TOKEN_RESOURCE,
            self._clientId,
            clientSecret,
            username,
            password
        )

        return TTLock.__send_request__(_url_request,'POST').json()
    
    def refresh_token(cls,clientId,clientSecret,refresh):
        ## This method refreshes an access token, based on :
        ## clientSecret (from TTAPI website) - relevant to app on website (not the actual app)
        ## username - user's username
        ## password - user's password
        ## hashed_password - if the user's password is already MD5 hashed, pass in true
        
        _url_request = TOKEN_REFRESH_URL.format(
            self._endpoint,
            TOKEN_RESOURCE,
            self._clientId,
            clientSecret,
            refresh
        )

        return TTLock.__send_request__(_url_request,'POST').json()
    
    ## -------
    ## End OAuth2 Token Functions
    ## -------
    
    
    def create_user(cls,clientId,clientSecret,username,password):
        
        ## This method creates a user, based on :
        ## clientSecret (from TTAPI website) - relevant to app on website (not the actual app)
        ## username - user's username
        ## password - user's password
        
        if (not password.islower()) or len(password)>32 or len(username)==0 or username.strip()=='':
            raise TTlockAPIError("Password is longer than 32 chars, username is empty in create_user")

        _url_request = USER_CREATE_URL.format(
            self._endpoint,
            USER_RESOURCE,
            self._clientId,
            clientSecret,
            username,
            hashlib.md5(password.encode()).hexdigest(),
            TTLock.__get_current_millis__(),
        )

        return TTLock.__send_request__(_url_request).json()


    ## -------
    ## Gateway Methods
    ## -------
    
    def get_gateway_generator(self,pageSize=20):
        ## Get a list of gateways, return a generator of gateways.  Each gateway appears to correspond to a specific physical gateway (that I know of)
        
        pageNo = 1
        totalPages = 1
        
        while TTLock.__verify_page__(pageNo, totalPages):
            _url_request = GATEWAY_LIST_URL.format(
                self._endpoint,
                GATEWAY_LIST_RESOURCE,
                self._clientId,
                self._accessToken,
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
        ## Get a list of locks associated with a gateway, returning a generator.  Each gateway appears to correspond to a specific physical gateway (that I know of)
        if not gatewayId:
            raise TTlockAPIError("No gateway ID Provided for get locks by gateway")

        _url_request = LOCKS_PER_GATEWAY_URL.format(
            self._endpoint,
            LOCKS_PER_GATEWAY_RESOURCE,
            self._clientId,
            self._accessToken,
            gatewayId,
            TTLock.__get_current_millis__(),
        )
        
        for lock in TTLock.__send_request__(_url_request).json().get(LIST_FIELD):
            yield lock

    ## -------
    ## End Gateway Methods
    ## -------


    ## -------
    ## Lock Methods
    ## -------

    
    def lock_state(self,lockId=None):
        if not lockId:
            raise TTlockAPIError("No lock ID Provided to get lock state")
        _url_request = LOCK_QUERY_URL.format(
            self._endpoint,
            LOCK_STATE_RESOURCE,
            self._clientId,
            self._accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__send_request__(_url_request).json().get(STATE_FIELD)
        
    def is_locked(self,lockId=None):
        state = self.lock_state(lockId)
        if state == 0:
            return True
        else:
            return False
    
    def lock_battery_status(self,lockId=None):
        if not lockId:
            raise TTlockAPIError("No lock ID Provided to get battery status")
        _url_request = LOCK_QUERY_URL.format(
            self._endpoint,
            LOCK_ELECTRIC_QUANTITY_RESOURCE,
            self._clientId,
            self._accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__send_request__(_url_request).json().get(ELECTRIC_QUANTITY_FIELD)
    
    def lock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError("No lock ID Provided to lock")

        _url_request = LOCK_QUERY_URL.format(
            self._endpoint,
            LOCK_RESOURCE,
            self._clientId,
            self._accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__is_erro_code_success__(TTLock.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))

    def unlock(self,lockId=None):
        if not lockId:
            raise TTlockAPIError("No lock ID Provided to unlock")

        _url_request = LOCK_QUERY_URL.format(
            self._endpoint,
            UNLOCK_RESOURCE,
            self._clientId,
            self._accessToken,
            lockId,
            TTLock.__get_current_millis__(),
        )
        return TTLock.__is_erro_code_success__(TTLock.__send_request__(_url_request).json().get(ERROR_CODE_FIELD))
    
    def get_lock_records_generator(self,lockId=None,pageSize=20,startDate=0,endDate=0):
        ## Get a list of lock records associated with a lock, return a generator of gateways.  Each gateway appears to correspond to a specific physical gateway (that I know of)
        if not lockId:
            raise TTlockAPIError("No lock ID Provided to get lock records")

        pageNo = 1
        totalPages = 1
        while TTLock.__verify_page__(pageNo, totalPages):
            _url_request = LOCK_RECORDS_URL.format(
                self._endpoint,
                LOCK_RECORDS_RESOURCE,
                self._clientId,
                self._accessToken,
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
    ## -------
    ## End Lock Methods
    ## -------
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