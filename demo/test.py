import requests
import json

# all_ddos = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo').json()

# print(json.dumps(all_ddos, sort_keys=True, indent=4))

metadata = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo/did:op:b07a8bb80242752ce164560ABCb6517DA90a4F65').json()
print(json.dumps(metadata, sort_keys=True, indent=4))