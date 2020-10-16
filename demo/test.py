import requests
import json

all_ddos = requests.get('https://aquarius.rinkeby.v3.dev-ocean.com/api/v1/aquarius/assets/ddo').json()

print(json.dumps(all_ddos, sort_keys=True, indent=4))

# metadata = requests.get('https://aquarius.rinkeby.v3.dev-ocean.com/api/v1/aquarius/assets/metadata/did:op:145c8961fa147a4147D829De72ef760E0a9d8304').json()
# print(json.dumps(metadata, sort_keys=True, indent=4))