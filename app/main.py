from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

def check_val(dict, key):
    try:
        value = dict[key]
        return True
    except KeyError:
        return False

'''
API to fetch all datatokens with their attributes
'''
@app.route('/datatokens')
def get_datatokens():
    '''
    totalMarketCap:  total marketCap of ocean datatokens
    totalLiquidityOcean:  total oceans locked in liquidity pools of datatokens
    totalLiquidity:  sum of total data tokens in liquidity pools * their price (basically how much in USD is datatokens in liquidity pools worth)
    oceanPrice:  ocean token price
    oceanMarketCap:  ocean protocol marketcap
    circulatingSupply:  no of tokens in circulation
    priceOcean:  price of datatoken in ocean
    price:  price of datatoken in usd
    lockedOcean:  ocean tokens in liquidity pool
    '''
    # Initializing
    tokens = []
    totalMarketCap = 0
    totalLiquidityOcean = 0
    totalLiquidity = 0

    # Fetching all ddos
    allData = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo')
    allData = json.loads(allData.content.decode('utf-8'))
    

    # Fetching ocean token info from coingecko
    data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ocean-protocol&vs_currencies=usd&include_market_cap=true')
    data = json.loads(data.content.decode('utf-8'))
    oceanPrice = data["ocean-protocol"]["usd"]
    oceanMarketCap = data["ocean-protocol"]["usd_market_cap"]

    for data in allData:
        token = {}
        did = data["id"]
        value = data
        print(value["isInPurgatory"])
        if value["isInPurgatory"] == 'false':
            name = value["dataTokenInfo"]["name"]
            symbol = value["dataTokenInfo"]["symbol"]
            circulatingSupply = value["dataTokenInfo"]["totalSupply"]
            priceOcean = value["price"]["value"]
            price = priceOcean * oceanPrice
            lockedOcean = data["price"]["ocean"]
            poolTokens = data["price"]["datatoken"]
            liquidity = poolTokens * price

            marketCap = price * circulatingSupply
            totalMarketCap = totalMarketCap + marketCap
            totalLiquidityOcean = lockedOcean + totalLiquidityOcean
            totalLiquidity = totalLiquidity + liquidity
            tags = value["service"][0]["attributes"]["additionalInformation"]
            if check_val(tags, "tags"):
                tags = tags["tags"]
            else:
                tags = []

            token = {"did": did, "name": name, "symbol": symbol, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "tags": tags, "liquidityOcean": lockedOcean}
            tokens.append(token)
    return jsonify(tokens, { "dataTokensMarketCap" : totalMarketCap, "dataTokensLiquidity" : totalLiquidity, "totalLiquidityOcean": totalLiquidityOcean, "oceanPrice": oceanPrice, "oceanMarketCap": oceanMarketCap })

'''
API to fetch any datatoken with its attributes given a DID
'''
@app.route('/datatoken/<did>')
def get_token(did):
    '''
    oceanPrice:  ocean token price
    circulatingSupply:  no of tokens in circulation
    maxSupply:  no of max tokens that could be in circulation
    priceOcean:  price of datatoken in ocean
    price:  price of datatoken in usd
    totalOcean:  ocean tokens in liquidity pool
    fullyDilutedValuation: Marketcap assuming max supply of datatoken
    priceHistory: Price history of given datatoken
    '''

    # Fetching ddo from given DID 
    data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo/' + did)
    data = json.loads(data.content.decode('utf-8'))
    token = {}

    if data["isInPurgatory"] == 'false':
        token = {}
        createdAt = data["created"]
        address = data["dataToken"]
        maxSupply = data["dataTokenInfo"]["cap"]
        name = data["dataTokenInfo"]["name"]
        symbol = data["dataTokenInfo"]["symbol"]
        circulatingSupply = data["dataTokenInfo"]["totalSupply"]
        priceOcean = data["price"]["value"]
        description = data["service"][0]["attributes"]["additionalInformation"]["description"]
        tags = data["service"][0]["attributes"]["additionalInformation"]
        if check_val(tags, "tags"):
            tags = tags["tags"]
        else:
            tags = []
        author = data["service"][0]["attributes"]["main"]["author"]
        datasetName = data["service"][0]["attributes"]["main"]["name"]
        pools = data["price"]["pools"]
        totalOcean = data["price"]["ocean"]

        data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ocean-protocol&vs_currencies=usd&include_market_cap=true')
        data = json.loads(data.content.decode('utf-8'))
        oceanPrice = data["ocean-protocol"]["usd"]
        price = priceOcean * oceanPrice

        marketCap = priceOcean * circulatingSupply * oceanPrice
        fullyDilutedValuation = priceOcean * maxSupply * oceanPrice
        price_history = []

        # Fetching price history
        if len(pools) > 0 and pools[0]:
            data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/pools/history/' + pools[0])
            data = json.loads(data.content.decode('utf-8'))
            price_history = data["datatokenPriceHistory"]

        token = {"did": did, "name": name, "symbol": symbol, "maxSupply": maxSupply, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "createdAt": createdAt, "address": address, "description": description, "tags": tags, "author": author, "datasetName": datasetName, "pools": pools, "liquidityOcean": totalOcean, "priceOcean": priceOcean, "fullyDilutedValuation": fullyDilutedValuation, "priceHistory": price_history}
    return jsonify(token)
