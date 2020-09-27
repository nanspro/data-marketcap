from ocean_lib.ocean.util import to_base_18
from create_datatoken import ocean, alice_wallet, data_token, token_address

pool = ocean.pool.create(
   token_address,
   data_token_amount=500.0,
   OCEAN_amount=5.0,
   from_wallet=alice_wallet
)
pool_address = pool.address
print(f'DataToken @{data_token.address} has a `pool` available @{pool_address}')