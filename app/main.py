from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

class dict(dict):

  def dig(self, *keys):
        try:
            for key in keys:
                self = self[key]
            return self
        except:
          return None

@app.route('/datatokens')
def get_datatokens():
    data = requests.get('https://aquarius.rinkeby.v3.dev-ocean.com/api/v1/aquarius/assets/ddo')
    data = json.loads(data.content.decode('utf-8'))
    tokens = []
    for id in data:
        token = {}
        did = id
        value = dict(data[id])
        createdAt = value["created"]
        address = value["dataToken"]
        
        # copyrightHolder = value.dig("service", "attributes", "additionalInformation", "copyrightHolder")
        # description = value["service"]["attributes"]["additionalInformation"]["description"]
        # author = value["service"]["attributes"]["main"]["author"]

        token = {"did": did, "createdAt": createdAt, "address": address} # "copyrightHolder": copyrightHolder, "description": description, "author": author}
        tokens.append(token)
    print(tokens)
    return jsonify(tokens)

@app.route('/token/')
def get_token(name):
    data = []
    # Fetch from aquarius elasticsearch events
    return data
