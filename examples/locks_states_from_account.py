import sys
from ttlock.io.ttlockwrapper import TTLock

""" 
To call this script:
pip3 install ttlockio
python3 locks_states_from_account.py YOUR_TTLOCK_CLIENT_ID YOUR_TTLOCK_TOKEN
"""

if __name__ == "__main__":
    clientId = str(sys.argv[1])
    token = str(sys.argv[2])
    ttlock = TTLock(clientId,token)
    
    gateways = []
    for gatewayPage in ttlock.generate_gateways():
        gateways = gateways+gatewayPage

    locks = []
    for gateway in gateways:
        locks = [lock for lock in ttlock.locks_gateway_list(gateway.get("gatewayId"))]
    
    for lock in locks:
        print('Eletrict quantity: {} %'.format(ttlock.lock_electric_quantity(lock.get('lockId'))))
        print('Lock State: {}'.format(ttlock.lock_state(lock.get('lockId'))))