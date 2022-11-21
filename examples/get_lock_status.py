import sys
sys.path.append(".")
sys.path.append("..")

from ttlockwrapper import TTLock

""" 
To call this script:
- Copy this file to your computer
$ pip3 install ttlockio
$ python3 locks_states_from_account.py YOUR_TTLOCK_CLIENT_ID YOUR_TTLOCK_TOKEN
"""

if __name__ == "__main__":
    clientId = str(sys.argv[1])
    clientSecret = str(sys.argv[2])
    username = str(sys.argv[3])
    password = str(sys.argv[4])
    

    myTTLock = TTLock(clientId)
    
    try:
        response = myTTLock.get_token(clientSecret, username, password)
        access_token = response["access_token"]
        refresh_token = response["refresh_token"]
        expires_in = response["expires_in"]
    except Exception as e:
        raise e
    
    myTTLock.accessToken = access_token
    
    print(f"My access token is {access_token} , refresh token is {refresh_token} , expires in (millis) {expires_in}")
    
    for gateway in myTTLock.get_gateway_generator():
        print(gateway)
        gwid = gateway["gatewayId"]
        for lock in myTTLock.get_locks_per_gateway_generator(gwid):
            lockid = lock["lockId"]
            print(myTTLock.is_locked(lockid))
            print(myTTLock.lock_battery_status(lockid))