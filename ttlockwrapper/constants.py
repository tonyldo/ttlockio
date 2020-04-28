
GOOD_HTTP_CODES = [200, 201, 202, 203]
TOKEN_ERROR_CODES = [10003]
ERROR_CODE_FIELD = 'errcode'
API_URI='https://api.ttlock.com/v3'
GATEWAY_LIST_RESOURCE = 'gateway/list'
LOCKS_PER_GATEWAY_RESOURCE = 'gateway/listLock'
LOCK_RECORDS_RESOURCE = 'lockRecord/list'
GATEWAY_LIST_URL = 'https://{}/{}?client_id={}&accessToken={}&pageNo={}&pageSize={}&date={}'
LOCKS_PER_GATEWAY_URL = 'https://{}/{}?client_id={}&accessToken={}&gatewayId={}&date={}'
LOCK_RECORDS_URL = 'https://{}/{}?client_id={}&accessToken={}&lockId={}&pageNo={}&pageSize={}&startDate={}&endDate={}&date={}'
