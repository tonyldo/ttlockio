# tests/test_ttlockwrapper.py

import ttlockwrapper
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
        m.register_uri('GET', re.compile(ttlockwrapper.constants.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)

    assert isinstance(response, list)
    assert response[0].get('gatewayId')==34144
    assert response[1].get('gatewayId')==35155

def test_ttlock_get_gateways_list_single_page():
    """Tests API call to get a gateways from a account""" 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.constants.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                   ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=2,pageSize=1)

    assert isinstance(response, list)
    assert len(response)==1
    assert response[0].get('gatewayId')==35155
    
def test_ttlock_get_gateways_list_expired_token():
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttlockerror:
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.constants.GATEWAY_LIST_RESOURCE)
            , text=INVALID_TOKEN_RESPONSE, status_code=200)
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)
        assert ttlockerror.error_code in TOKEN_ERROR_CODES

def test_ttlock_get_gateways_list_invalid_request():
    with pytest.raises(requests.HTTPError):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.constants.GATEWAY_LIST_RESOURCE)
            , text=' ', status_code=400)
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)


def test_ttlock_get_locks_gateway_list():
    with open(MOCK_JSON_PATH+'gateway_lock_list_response.json', 'r') as json_file:
        mock_response = json_file.read() 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCKS_PER_GATEWAY_RESOURCE), text=mock_response)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).locks_gateway_list(gatewayId=35155)

    assert isinstance(response, list)
    assert response[0].get('lockId' )==3879122
    assert response[1].get('lockId' )==1928723

def test_ttlock_get_locks_gateway_list_invalid_gatewayId():
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCKS_PER_GATEWAY_RESOURCE), text='')
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).locks_gateway_list()

def test_ttlock_get_lock_records_list_paginated():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCK_RECORDS_RESOURCE), text=response_lock_records_list_callback)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).lock_records_list(lockId=1928723,pageNo=1,pageSize=20)

    assert isinstance(response, list)
    assert len(response)==80

def test_ttlock_get_lock_records_list__invalid_lock_id():
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCK_RECORDS_URL), text='')
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).lock_records_list()

def test_ttlock_get_lock_state():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCK_STATE_RESOURCE), text=LOCK_STATE_RESPONSE)
        state = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).lock_state(lockId=1928723)
    assert state == 1 

def test_ttlock_get_lock_electric_quantity():
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.constants.LOCK_ELECTRIC_QUANTITY_RESOURCE), text=LOCK_ELECTRIC_QUANTITY_RESPONSE)
        electric_quantity = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
        ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity(lockId=1928723)
    assert electric_quantity == 68 


def test_ttlock_no_mock_request():
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=20)
        assert response.status_code in ttlockwrapper.constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR
    
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).locks_gateway_list()
        assert response.status_code in ttlockwrapper.constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR
    
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_records_list(pageNo=1,pageSize=20)
        assert response.status_code in ttlockwrapper.constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR  
    
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_state()
        assert response.status_code in ttlockwrapper.constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR
    
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity()
        assert response.status_code in ttlockwrapper.constants.GOOD_HTTP_CODES
        assert not ttLock_error.error_code == INVALID_CURRENT_TIMESTAMP_ERROR

def test_ttlock_no_mock_invalid_date_current():
    with pytest.raises(ttlockwrapper.ttlock.TTlockAPIError) as ttLock_error:
        _url_request = ttlockwrapper.constants.GATEWAY_LIST_URL.format(
            ttlockwrapper.constants.API_URI,
            ttlockwrapper.constants.GATEWAY_LIST_RESOURCE,
            FAKE_CLIENT_ID,
            FAKE_ACCESS_TOKEN,
            1,
            20,
            ttlockwrapper.TTLock().__get_current_millis__()-10000,
        )
        ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                    ,accessToken=FAKE_ACCESS_TOKEN).lock_electric_quantity()
        assert ttLock_error.error_code==INVALID_CURRENT_TIMESTAMP_ERROR