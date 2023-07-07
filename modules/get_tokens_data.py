import requests
import asyncio
import json
import os
from modules.check_balance import main
from modules.get_chain_and_rpc import chain
from dotenv import load_dotenv

load_dotenv()

api_1inch = 'https://api.1inch.io/v5.0/'
wallet = os.getenv('PRIVATE_ADDRESS')

def get_tokens_data():

    url = f'{api_1inch}{chain}/tokens'
    response = requests.get(url)
    token_data = response.json()

    tokens = []

    for token in token_data['tokens']:
        name = token_data['tokens'][token]['name']
        address = token_data['tokens'][token]['address']
        symbol = token_data['tokens'][token]['symbol']
        decimals = token_data['tokens'][token]['decimals']
        token = {
            'name': name,
            'symbol': symbol,
            'address': address,
            'decimals': decimals
        }
        tokens.append(token)

    with open('./json_files/tokens.json', 'w') as f:
        json.dump(tokens, f, indent=4)

    asyncio.run(main())
