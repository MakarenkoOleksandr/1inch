import json
import requests

chain_id = 56


def get_native_token_address():

    url = f'https://api.1inch.io/v5.0/{chain_id}/tokens'
    response = requests.get(url)
    token_data = response.json()

    for token in token_data['tokens']:
        name = token_data['tokens'][token]['name']
        address = token_data['tokens'][token]['address']
        symbol = token_data['tokens'][token]['symbol']
        if address == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            token = {
                'name': name,
                'symbol': symbol,
            }
            break

    with open('native_token.json', 'w') as f:
        json.dump(token, f, indent=4)


get_native_token_address()
