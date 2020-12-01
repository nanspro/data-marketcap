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

@app.route('/datatokens')
def get_datatokens():
    allData = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo')
    allData = json.loads(allData.content.decode('utf-8'))
    tokens = []
    totalMarketCap = 0
    # totalVolume = 0
    totalLiquidityOcean = 0
    totalLiquidity = 0
    data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ocean-protocol&vs_currencies=usd&include_market_cap=true')
    data = json.loads(data.content.decode('utf-8'))
    oceanPrice = data["ocean-protocol"]["usd"] # ocean token price
    oceanMarketCap = data["ocean-protocol"]["usd_market_cap"] # ocean protocol marketcap
    for data in allData:
        token = {}
        did = data["id"]
        value = data
        name = value["dataTokenInfo"]["name"]
        symbol = value["dataTokenInfo"]["symbol"]
        circulatingSupply = value["dataTokenInfo"]["totalSupply"] # how many tokens in circulation
        priceOcean = value["price"]["value"] # price of datatoken in ocean
        price = priceOcean * oceanPrice # price of datatoken in usd
        lockedOcean = data["price"]["ocean"] # ocean tokens in liquidity pool
        poolTokens = data["price"]["datatoken"]
        liquidity = poolTokens * price

        # volume = value["price"]["datatoken"] * price
        marketCap = price * circulatingSupply
        totalMarketCap = totalMarketCap + marketCap # total marketCap of ocean datatokens
        totalLiquidityOcean = lockedOcean + totalLiquidityOcean # total oceans locked in liquidity pools of datatokens
        totalLiquidity = totalLiquidity + liquidity # sum of total data tokens in liquidity pools * their price (basically how much in USD is datatokens in liquidity pools worth)
        # totalVolume = totalVolume + volume
        tags = value["service"][0]["attributes"]["additionalInformation"]
        if check_val(tags, "tags"):
            tags = tags["tags"]
        else:
            tags = []
        # copyrightHolder = value.dig("service", "attributes", "additionalInformation", "copyrightHolder")
        # description = value["service"]["attributes"]["additionalInformation"]["description"]
        # author = value["service"]["attributes"]["main"]["author"]

        token = {"did": did, "name": name, "symbol": symbol, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "tags": tags, "liquidityOcean": lockedOcean}
        tokens.append(token)
    # print(tokens)
    return jsonify(tokens, { "dataTokensMarketCap" : totalMarketCap, "dataTokensLiquidity" : totalLiquidity, "totalLiquidityOcean": totalLiquidityOcean, "oceanPrice": oceanPrice, "oceanMarketCap": oceanMarketCap })

@app.route('/datatoken/<did>')
def get_token(did):
    data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo/' + did)
    data = json.loads(data.content.decode('utf-8'))
    token = {}
    createdAt = data["created"]
    address = data["dataToken"]
    maxSupply = data["dataTokenInfo"]["cap"] # how many datatokens will ever be (at max)
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
    totalOcean = data["price"]["ocean"] # total no of ocean tokens in liquidity pool
    # volume = data["price"]["datatoken"]

    data = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ocean-protocol&vs_currencies=usd&include_market_cap=true')
    data = json.loads(data.content.decode('utf-8'))
    oceanPrice = data["ocean-protocol"]["usd"]
    price = priceOcean * oceanPrice

    marketCap = priceOcean * circulatingSupply * oceanPrice
    fullyDilutedValuation = priceOcean * maxSupply * oceanPrice
    price_history = []
    if pools[0]:
        data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/pools/history/' + pools[0])
        data = json.loads(data.content.decode('utf-8'))
        price_history = data["oceanAddRemove"]

    token = {"did": did, "name": name, "symbol": symbol, "maxSupply": maxSupply, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "createdAt": createdAt, "address": address, "description": description, "tags": tags, "author": author, "datasetName": datasetName, "pools": pools, "liquidityOcean": totalOcean, "priceOcean": priceOcean, "fullyDilutedValuation": fullyDilutedValuation, "priceHistory": price_history}

    # Fetch from aquarius elasticsearch events
    return jsonify(token)
