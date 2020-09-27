from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

@app.route('/datatokens')
def get_datatokens():
    data = requests.get('https://aquarius.rinkeby.v3.dev-ocean.com/api/v1/aquarius/assets/ddo')
    data = data.content
    # Structure response
    return data

@app.route('/token/<name>')
def get_token(name):
    data = []
    # Query balancer subgraph at rinkeby and structure data response
    # OR
    # Directly fetch price from balancer contracts (but how to get proper historical prices?)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=20000)
