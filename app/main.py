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
    data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo')
    data = json.loads(data.content.decode('utf-8'))
    tokens = []
    for id in data:
        token = {}
        did = id
        value = dict(data[id])
        name = value["dataTokenInfo"]["name"]
        symbol = value["dataTokenInfo"]["symbol"]
        circulatingSupply = value["dataTokenInfo"]["totalSupply"]
        price = value["price"]["value"]
        volume = value["price"]["datatoken"] * price
        marketCap = price * circulatingSupply
        tags = value["service"][0]["attributes"]["additionalInformation"]
        if check_val(tags, "tags"):
            tags = tags["tags"]
        else:
            tags = []
        # copyrightHolder = value.dig("service", "attributes", "additionalInformation", "copyrightHolder")
        # description = value["service"]["attributes"]["additionalInformation"]["description"]
        # author = value["service"]["attributes"]["main"]["author"]

        token = {"did": did, "name": name, "symbol": symbol, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "volume": volume, "tags": tags}
        tokens.append(token)
    # print(tokens)
    return jsonify(tokens)

@app.route('/datatoken/<did>')
def get_token(did):
    data = requests.get('https://aquarius.mainnet.oceanprotocol.com/api/v1/aquarius/assets/ddo/' + did)
    data = json.loads(data.content.decode('utf-8'))
    token = {}
    createdAt = data["created"]
    address = data["dataToken"]
    supplyCap = data["dataTokenInfo"]["cap"]
    name = data["dataTokenInfo"]["name"]
    symbol = data["dataTokenInfo"]["symbol"]
    circulatingSupply = data["dataTokenInfo"]["totalSupply"]
    price = data["price"]["value"]
    marketCap = price * circulatingSupply
    description = data["service"][0]["attributes"]["additionalInformation"]["description"]
    tags = data["service"][0]["attributes"]["additionalInformation"]["tags"]
    author = data["service"][0]["attributes"]["main"]["author"]
    datasetName = data["service"][0]["attributes"]["main"]["name"]
    pools = data["price"]["pools"]
    totalOcean = data["price"]["ocean"]
    volume = data["price"]["datatoken"]
    priceOcean = totalOcean/volume

    token = {"did": did, "name": name, "symbol": symbol, "circulatingSupply": circulatingSupply, "price": price, "marketCap": marketCap, "createdAt": createdAt, "supplyCap": supplyCap, "address": address, "description": description, "tags": tags, "author": author, "datasetName": datasetName, "pools": pools, "totalOcean": totalOcean, "priceOcean": priceOcean}

    # Fetch from aquarius elasticsearch events
    return jsonify(token)
