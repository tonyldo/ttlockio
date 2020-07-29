# API Urls
API_URI='https://api.ttlock.com/v3'
USER_API_URI = 'https://api.ttlock.com/v3/user/?'
LOCK_API_URI = 'https://api.ttlock.com/v3/lock/?'
EKEY_API_URI = 'https://api.ttlock.com/v3/key/'
PASSCODE_API_URI = 'https://api.ttlock.com/v3/keyboardPwd/?'
GATEWAY_API_URI = 'https://api.ttlock.com/v3/gateway/?'
ICCARD_API_URI = 'https://api.ttlock.com/v3/identityCard/?'
FINGERPRINT_API_URI = 'https://api.ttlock.com/v3/fingerprint/?'
UNLOCK_RECORD_API_URI = 'https://api.ttlock.com/v3/lockRecord/?'
WIRELESS_KEYBOARD_API_URI = 'https://api.ttlock.com/v3/wirelessKeypad/'

# FIELDS
ERROR_CODE_FIELD = 'errcode'
MENSSAGE_FIELD = 'errmsg'
LIST_FIELD = 'list'
STATE_FIELD = 'state'
PAGES_FIELD = 'pages'
GATEWAY_MAC_FIELD = 'gatewayMac'
LOCK_MAC_FIELD ='lockMac'
LOCK_ALIAS_FIELD = 'lockAlias'
LOCK_ID_FIELD = 'lockId'
GATEWAY_ID_FIELD = 'gatewayId'
ELECTRIC_QUANTITY_FIELD = 'electricQuantity'

# RESOURCES
LOCK_RESOURCE = 'lock/lock'
UNLOCK_RESOURCE = 'lock/unlock'
LOCKS_PER_GATEWAY_RESOURCE = 'gateway/listLock'
LOCK_RECORDS_RESOURCE = 'lockRecord/list'
LOCK_STATE_RESOURCE = 'lock/queryOpenState'
LOCK_ELECTRIC_QUANTITY_RESOURCE='lock/queryElectricQuantity'

# OTHERS
GOOD_HTTP_CODES = [200, 201, 202, 203]
GATEWAY_LIST_RESOURCE = 'gateway/list'
GATEWAY_LIST_URL = '{}/{}?clientId={}&accessToken={}&pageNo={}&pageSize={}&date={}'
LOCKS_PER_GATEWAY_URL = '{}/{}?clientId={}&accessToken={}&gatewayId={}&date={}'
LOCK_RECORDS_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&pageNo={}&pageSize={}&startDate={}&endDate={}&date={}'
LOCK_QUERY_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&date={}'