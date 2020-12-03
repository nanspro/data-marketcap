# Data-Marketcap
Data Tokens are data specific tokens which are built upon ocean protocol and ethereum.

Data Market Cap provides a fundamental analysis of the data tokens market such as price, metadata and marketcap. It aims to be an aggregrator for all the information about data tokens. Currently data tokens can only be bought and sold at balancer so the price and volume is derived from there. The website will keep updating itself as data tokens become more popular and are traded heavily on other DEXs and CEXs.

Data-Marketcap is currently hosted at http://datamarketcap.xyz/ The code for the frontend is open sourced and can be found here https://github.com/nemani/dmc
## Local Setup
- Create a python virtual environment and then after activating, install dependencies from requirements.txt like this
    
        `pip install -r requirements.txt`
- Run the backend server
        
        `python wsgi.py`
        Will start the backend server

## Backend APIs

**Fetch all datatokens**

Datatokens attributes on the home page
```text
totalMarketCap:  total marketCap of ocean datatokens
totalLiquidityOcean:  total oceans locked in liquidity pools of datatokens
totalLiquidity:  sum of total data tokens in liquidity pools * their price (basically how much in USD is datatokens in liquidity pools worth)
oceanPrice:  ocean token price
oceanMarketCap:  ocean protocol marketcap
circulatingSupply:  no of tokens in circulation
priceOcean:  price of datatoken in ocean
price:  price of datatoken in usd
lockedOcean:  ocean tokens in liquidity pool
```

**Fetch a datatoken given DID**
Datatoken attributes that will be shown on datatoken page
```text
oceanPrice:  ocean token price
circulatingSupply:  no of tokens in circulation
maxSupply:  no of max tokens that could be in circulation
priceOcean:  price of datatoken in ocean
price:  price of datatoken in usd
totalOcean:  ocean tokens in liquidity pool
fullyDilutedValuation: Marketcap assuming max supply of datatoken
priceHistory: Price history of given datatoken
```
## LICENSE
[MIT](https://github.com/nanspro/data-marketcap/blob/master/LICENSE)