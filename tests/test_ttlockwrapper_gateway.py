# tests/test_ttlockwrapper.py

import ttlockwrapper
import requests_mock
import re
import pytest

FAKE_CLIENT_ID='34144ff6749ea9ced96cbd2470db12f2'
FAKE_ACCESS_TOKEN='cc8d7ab5acb3b65998cec69129235155'

def response_gateway_list_callback(request, context):
    pageNo = re.compile('pageNo=\\d').search(request.url).group()[7:]
    with open('./tests/gateway_response_page_{}.json'.format(pageNo), 'r') as json_file:
        mock_response = json_file.read()
    return mock_response
    
def test_ttlock_get_gateways_list_paginated():
    """Tests API call to get a gateways from a account""" 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.ttlock.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)

    assert isinstance(response, list)
    assert response[0].get('gatewayId')==34144
    assert response[1].get('gatewayId')==35155

def test_ttlock_get_gateways_list():
    """Tests API call to get a gateways from a account""" 
    with requests_mock.Mocker() as m:
        m.register_uri('GET', re.compile(ttlockwrapper.ttlock.GATEWAY_LIST_RESOURCE), text=response_gateway_list_callback)
        response = ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
                     ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=2,pageSize=1)

    assert isinstance(response, list)
    assert len(response)==1
    assert response[0].get('gatewayId')==35155
    
def test_ttlock_get_gateways_list_expired_token():
    with pytest.raises(PermissionError):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.ttlock.GATEWAY_LIST_RESOURCE)
            , text='{"errcode": 10003,"errmsg": "invalid token","description": ""}', status_code=200)
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)

def test_ttlock_get_gateways_list_date_current():
    with pytest.raises(ValueError):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.ttlock.GATEWAY_LIST_RESOURCE)
            , text='{"errcode": 80000,"errmsg": "date must be current time","description": ""}', status_code=200)
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)

def test_ttlock_get_gateways_list_invalid_request():
    with pytest.raises(Exception, match=r'HTTP_ERROR'):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', re.compile(ttlockwrapper.ttlock.GATEWAY_LIST_RESOURCE)
            , text=' ', status_code=400)
            ttlockwrapper.TTLock(clientId=FAKE_CLIENT_ID
            ,accessToken=FAKE_ACCESS_TOKEN).gateways_list(pageNo=1,pageSize=1)