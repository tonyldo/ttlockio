import sys
sys.path.append(".")

from ttlockwrapper import TTLock

""" 
To call this script:
$ git clone this_repo
$ pip3 install -r requirements.txt
$ python3 examples/locks_states_from_account.py YOUR_TTLOCK_CLIENT_ID YOUR_TTLOCK_TOKEN
"""

if __name__ == "__main__":
    clientId = str(sys.argv[1])
    token = str(sys.argv[2])
    ttlock = TTLock(clientId,token)

    gateways = [gateway for gateway in ttlock.get_gateway_generator()]

    locks = []
    for gateway in gateways:
        locks += [lock for lock in ttlock.get_locks_per_gateway_generator(gateway.get("gatewayId"))]
    
    for lock in locks:
        print('Eletrict quantity: {}%'.format(ttlock.lock_electric_quantity(lock.get('lockId'))))
        print('Lock State: {}'.format(ttlock.lock_state(lock.get('lockId'))))