from variables import wallet, web3, converter_private
from web3 import Web3
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Session
from decimal import Decimal, ROUND_HALF_UP

with open('./json_files/tokens.json') as f:
    tokens = json.load(f)

with open('./json_files/erc20.json') as f:
    token_abi = json.load(f)

w3 = web3


def get_balance(token, wallet):
    token_contract = w3.eth.contract(
        address=Web3.to_checksum_address(token), abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet).call()

    return balance


def converter_to_usd(token_name, token_symbol, token_balance):
    url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

    parameters = {
        'amount': token_balance,
        'symbol': token_symbol
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': converter_private,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()
        price = Decimal(data['data'][0]['quote']['USD']['price'])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    balance_in_usd = price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
    print(
        f"Баланс токена {token_name}: ~ {token_balance} ~ {balance_in_usd} $")


def get_tokens_balance():
    native_token_balance = w3.eth.get_balance(wallet)
    native_token_balance = w3.from_wei(native_token_balance, 'ether')
    for token in tokens:
        if token['address'] == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            native_token_balance = converter_to_usd(
                tokens[0]['name'], tokens[0]['symbol'], native_token_balance)

        else:
            token_balance = get_balance(token['address'], wallet)
            if token_balance > 0:
                token_balance = w3.from_wei(token_balance, 'ether')
                token_balance = converter_to_usd(
                    token['name'], token['symbol'], token_balance)
