# tests/test_py

from ttlockwrapper import TTLock,TTlockAPIError, constants
import requests_mock
import requests
import re
import pytest

FAKE_CLIENT_ID='34144ff6749ea9ced96cbd2470db12f2'
FAKE_ACCESS_TOKEN='cc8d7ab5acb3b65998cec69129235155'
TOKEN_ERROR_CODES = [10003]
INVALID_CURRENT_TIMESTAMP_ERROR = 80000
LOCK_STATE_RESPONSE = '{"state": 1}'
LOCK_ELECTRIC_QUANTITY_RESPONSE = '{"electricQuantity": 68}'
INVALID_TOKEN_RESPONSE = '{"errcode": 10003,"errmsg": "invalid token","description": ""}'
MOCK_JSON_PATH = './tests/data/'


def response_lock_records_list_callback(request, context):
    pageNo = re.compile('pageNo=\\d').search(request.url).group()[7:]
    with open(MOCK_JSON_PATH+'lock_records_response_page_{}.json'.format(pageNo), 'r') as json_file:
        mock_response = json_file.read()
    return mock_response

def response_gateway_list_callback(request, context):
    pageNo = re.compile('pageNo=\\d').search(request.url).group()[7:]
    with open(MOCK_JSON_PATH+'gateway_response_page_{}.json'.format(pageNo), 'r') as json_file:
        mock_response = json_file.read()
    return mock_response
    
def test_ttlock_get_gateways_list_paginated():
    """Tests API call to get a gateways from a account""" 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response_generator = TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).get_gateway_generator(pageSize=1)
        gateways = [gateway for gateway in response_generator]
        assert len(gateways)==2

def test_ttlock_get_gateways_stop_iteration(mocker):
    """Tests API call to get a gateways from a account""" 
    with requests_mock.Mocker() as m:
        mocker.patch.object(TTLock, '__verify_page__') 
        TTLock.__verify_page__.return_value = False 
        m.register_uri('GET', re.compile(constants.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response_generator = TTLock(clientId=FAKE_CLIENT_ID
                   ,accessToken=FAKE_ACCESS_TOKEN).get_gateway_generator(pageSize=1)
        with pytest.raises(StopIteration): 
            next(response_generator) 

def test_ttlock_get_locks_gateway_list():
    with open(MOCK_JSON_PATH+'gateway_lock_list_response.json', 'r') as json_file:
        mock_response = json_file.read() 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.LOCKS_PER_GATEWAY_RESOURCE), text=mock_response)
        response_generator = TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).get_locks_per_gateway_generator(gatewayId=35155)
        lock_list = [lock for lock in response_generator]
    
    assert isinstance(lock_list, list)
    assert lock_list[0].get('lockId' )==3879122
    assert lock_list[1].get('lockId' )==1928723

def test_ttlock_get_lock_records_list_paginated():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.LOCK_RECORDS_RESOURCE), text=response_lock_records_list_callback)
        response_generator = TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).get_lock_records_generator(lockId=1928723,pageSize=20)
        record_list = [record for record in response_generator]
        assert len(record_list)==80

def test_ttlock_get_lock_state():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.LOCK_STATE_RESOURCE), text=LOCK_STATE_RESPONSE)
        state = TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).lock_state(lockId=1928723)
    assert state == 1 

def test_ttlock_get_lock_electric_quantity():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.LOCK_ELECTRIC_QUANTITY_RESOURCE), text=LOCK_ELECTRIC_QUANTITY_RESPONSE)
        electric_quantity = TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity(lockId=1928723)
    assert electric_quantity == 68 


def test_ttlock_no_mock_request():

    with pytest.raises(TTlockAPIError) as ttLock_error:
        response = TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_state()
        assert response.status_code in constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR
    
    with pytest.raises(TTlockAPIError) as ttLock_error:
        response = TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity()
        assert response.status_code in constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR

def test_ttlock_no_mock_invalid_date_current():
    with pytest.raises(TTlockAPIError) as ttLock_error:
        _url_request = constants.GATEWAY_LIST_URL.format(
            constants.API_URI,
            constants.GATEWAY_LIST_RESOURCE,
            FAKE_CLIENT_ID,
            FAKE_ACCESS_TOKEN,
            1,
            20,
            TTLock().__get_current_millis__()-10000,
        )
        TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity()
        assert ttLock_error.error_code==INVALID_CURRENT_TIMESTAMP_ERROR

def test_lock():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.LOCK_RESOURCE), text='{"errcode": 0,"errmsg": "none error message or means yes","description": "表示成功或是"}')
        assert TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).lock(lockId=1928723)

def test_unlock():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.UNLOCK_RESOURCE), text='{"errcode": 0,"errmsg": "none error message or means yes","description": "表示成功或是"}')
        assert TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).unlock(lockId=1928723)

def test__send_request__():
    with pytest.raises(requests.exceptions.HTTPError):   
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(constants.UNLOCK_RESOURCE), text='Not Found', status_code=403)
            assert TTLock(clientId=FAKE_CLIENT_ID,accessToken=FAKE_ACCESS_TOKEN).unlock(lockId=1928723)
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(constants.UNLOCK_RESOURCE), text='{"errcode": 0,"errmsg": "none error message or means yes","description": "表示成功或是"}')
        assert TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).unlock(lockId=1928723)    