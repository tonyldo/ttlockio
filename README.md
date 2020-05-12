# ttlock.io
Python wrapper for TTLock API

1. Register a developer account
```
https://open.ttlock.com/reg
```

2. Log in 
```
https://open.ttlock.com/login
```

3. Create application:
```
https://open.ttlock.com/manager/apps/create
```
- The application needs to be reviewed. After it is reviewed, all the APIs are available.

4. Create a user for this application:
```
$ curl --location --request POST 'https://api.ttlock.com/v3/user/register?clientId=YOUR_APP_CLIENT_ID&clientSecret=YOUR_APP_CLIENTSECRET&username=NEW_NAME_FOR_YOUR_USER&password=NEW_PASS_FOR_YOUR_USER&date=CURRENTMILLIS' \
--header 'Content-Type: application/x-www-form-urlencoded' \
```
- ATTENTION: you need pass the NEW_PASS_FOR_YOUR_USER with max 32 chars, low case and md5 encrypted

5. Test your USER:
- Download TTLock App at your cellphones app store. Log in with your UserName and Pass created on step four. Add your ttlock gateway and locks.

6. Get the AccessToken

```
$ curl --location --request POST 'https://api.ttlock.com/oauth2/token?client_id=YOUR_APP_CLIENT_ID&client_secret=YOUR_APP_CLIENTSECRET&username=NAME_FOR_YOUR_USER_CREATE_ON_LAST_STEP&password=NEW_PASS_FOR_YOUR_USER_CREATE_ON_LAST_STEP&grant_type=password&redirect_uri=https://yourdomain.com/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
```

7. Install and Use 
```
$ pip install ttlockio 
$ python3
>>import ttlockwrapper
>>TTLock(clientId=YOUR_CLIENT_ID,accessToken=YOUR_ACCESS_TOKEN).get_gateway_generator()
```