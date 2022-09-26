# ttlock.io
Python wrapper for TTLock API

1. Register a developer account
```
https://euopen.ttlock.com/register
```

2. Log in 
```
https://euopen.ttlock.com/login
```

3. Create application:
```
https://euopen.ttlock.com/CreateApplication
```
- The application needs to be reviewed. After it is reviewed, all the APIs are available.

4. Create a user for this application and get the access token:

```
$ pip install ttlockio
$ create_user YOUR_APP_CLIENT_ID YOUR_APP_CLIENT_SECRET USERNAME PASSWORD --token
```


`--token` is an optional parameter; `create_user -h` for usage. if not used the user will be created without an access token. You need pass the PASSWORD with max 32 chars, low case

- Return:

```
{'username': 'prefixed_user'}
{'access_token': 'xxx', 'uid': xxx, 'refresh_token': 'xxx', 'openid': xxx, 'scope': 'user,key,room', 'token_type': 'Bearer', 'expires_in': 7776000}
```

5a. Refresh the access token when required

```
refresh_access_token YOUR_APP_CLIENT_ID YOUR_APP_CLIENT_SECRET YOUR_REFRESH_TOKEN
```

- Return:

```
{'access_token': 'xxx', 'refresh_token': 'xxx', 'openid': xxx, 'scope': 'user,key,room', 'token_type': 'Bearer', 'expires_in': 7776000}
```


5. Test your USER:
- Download TTLock App at your cellphones app store. Log in with your YOUR_APP_NAME_CONCAT_NEW_NAME_FOR_YOUR_USER and NEW_PASS_FOR_YOUR_USER created on step four. 
- Add your TTLock gateways and locks.

6. Install and Use 
```
$ pip install ttlockio 
$ python3
>>import ttlockwrapper
>>gateways = list(ttlockwrapper.TTLock(clientId='YOUR_APP_CLIENT_ID',accessToken='YOUR_ACCESS_TOKEN').get_gateway_generator())
>>print('Gateway ID and Gateway Lock quantity: {}, {}'.format(gateways[0].get('gatewayId'),gateways[0].get('lockNum')))
```

7. Examples
- See example dir at this repo.
