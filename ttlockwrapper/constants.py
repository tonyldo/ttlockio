
GOOD_HTTP_CODES = [200, 201, 202, 203]
USER_FIELD = 'username'
ACCESS_TOKEN_FIELD = 'access_token'
REFRESH_TOKEN_FIELD = 'refresh_token'
EXPIRE_TIME_TOKEN_FIELD = 'expires_in'
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
API_URI='https://euapi.ttlock.com/v3'
GATEWAY_LIST_RESOURCE = 'gateway/list'
LOCK_RESOURCE = 'lock/lock'
UNLOCK_RESOURCE = 'lock/unlock'
LOCKS_PER_GATEWAY_RESOURCE = 'gateway/listLock'
LOCK_RECORDS_RESOURCE = 'lockRecord/list'
LOCK_STATE_RESOURCE = 'lock/queryOpenState'
LOCK_ELECTRIC_QUANTITY_RESOURCE='lock/queryElectricQuantity'
GATEWAY_LIST_URL = '{}/{}?clientId={}&accessToken={}&pageNo={}&pageSize={}&date={}'
LOCKS_PER_GATEWAY_URL = '{}/{}?clientId={}&accessToken={}&gatewayId={}&date={}'
LOCK_RECORDS_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&pageNo={}&pageSize={}&startDate={}&endDate={}&date={}'
LOCK_QUERY_URL = '{}/{}?clientId={}&accessToken={}&lockId={}&date={}'

USER_RESOURCE = 'user/register'
USER_CREATE_URL = '{}/{}?clientId={}&clientSecret={}&username={}&password={}&date={}'

TOKEN_RESOURCE = 'oauth2/token'
TOKEN_CREATE_URL = 'https://euapi.ttlock.com/{}?client_id={}&client_secret={}&username={}&password={}&grant_type=password&redirect_uri={}'

TOKEN_REFRESH_URL = 'https://euapi.ttlock.com/{}?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token&redirect_uri={}'


UNLOCK_CODES = {1:'App unlock', 2:'touch the parking lock', 3:'gateway unlock', 4:'passcode unlock', 5:'parking lock raise', 6:'parking lock lower', 7:'IC card unlock', 8:'fingerprint unlock', 9:'wristband unlock', 10:'mechanical key unlock', 11:'Bluetooth lock', 12:'gateway unlock', 29:'unexpected unlock', 30:'door magnet close', 31:'door magnet open', 32:'open from inside', 33:'lock by fingerprint', 34:'lock by passcode', 35:'lock by IC card', 36:'lock by Mechanical key', 37:'Remote Control', 44:'Tamper alert', 45:'Auto Lock', 46:'unlock by unlock key', 47:'lock by lock key', 48:'Use INVALID Passcode several times'}