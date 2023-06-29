import json
import requests
from variables import api_1inch, chain
from wallet_balance.check_balance import get_tokens_balance


def get_tokens_data():

    url = f'{api_1inch}{chain}/tokens'
    response = requests.get(url)
    token_data = response.json()
    tokens = []

    for token in token_data['tokens']:
        name = token_data['tokens'][token]['name']
        address = token_data['tokens'][token]['address']
        symbol = token_data['tokens'][token]['symbol']
        token = {
            'name': name,
            'symbol': symbol,
            'address': address
        }
        tokens.append(token)

    with open('./json_files/tokens.json', 'w') as f:
        json.dump(tokens, f, indent=4)

    get_tokens_balance()
