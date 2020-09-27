from ocean_utils.agreements.service_factory import ServiceDescriptor

from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.ocean.util import to_base_18
from ocean_lib.data_provider.data_service_provider import DataServiceProvider

#Alice's config
config = {
   'network' : 'rinkeby',
   'metadataStoreUri' : 'https://aquarius.rinkeby.v3.dev-ocean.com/',
   'providerUri' : 'https://provider.rinkeby.v3.dev-ocean.com/'
}
ocean = Ocean(config)
alice_wallet = Wallet(ocean.web3, private_key='9d864647d271140c41a9bd0406d62152a10d1ddc1560fac65c824f8c35e2cfa5')

data_token = ocean.create_data_token(ocean.config.metadata_store_url, 'Rahul DataToken', 'RDT1', alice_wallet)
token_address = data_token.address
print(token_address)


# `ocean.assets.create` will encrypt the URLs using the provider's encrypt service endpoint and update 
# the asset before pushing to metadata store
# `ocean.assets.create` will require that token_address is a valid DataToken contract address, unless token_address
# is not provided then the `create` method will first create a new data token and use it in the new
# asset.
metadata =  {
    "main": {
        "type": "dataset", "name": "Monkey Species Data", "author": "Rahul", 
        "license": "CC0: Public Domain", "dateCreated": "2020-02-01T10:55:11Z", 
        "files": [
            { "index": 0, "contentType": "application/zip", "url": "https://s3.amazonaws.com/datacommons-seeding-us-east/10_Monkey_Species_Small/assets/training.zip"},
            { "index": 1, "contentType": "text/text", "url": "https://s3.amazonaws.com/datacommons-seeding-us-east/10_Monkey_Species_Small/assets/monkey_labels.txt"},
            { "index": 2, "contentType": "application/zip", "url": "https://s3.amazonaws.com/datacommons-seeding-us-east/10_Monkey_Species_Small/assets/validation.zip"}]}
}

# Prepare attributes for the download service including the cost in DataTokens
service_attributes = {
        "main": {
            "name": "dataAssetAccessServiceAgreement",
            "creator": alice_wallet.address,
            "cost": 1.0, # service cost is 1.0 tokens 
            "timeout": 3600 * 24,
            "datePublished": metadata["main"]['dateCreated']
        }
    }

service_endpoint = DataServiceProvider.get_download_endpoint(ocean.config)
download_service = ServiceDescriptor.access_service_descriptor(service_attributes, service_endpoint)
asset = ocean.assets.create(metadata, alice_wallet, service_descriptors=[download_service], data_token_address=token_address)
assert token_address == asset.data_token_address

did = asset.did
print(did)

data_token.mint_tokens(alice_wallet.address, 1000.0, alice_wallet)