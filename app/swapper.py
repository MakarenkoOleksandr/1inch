import json
import requests
from decimal import Decimal
import os
from web3 import Web3
from urllib.parse import urlencode
from eth_utils import to_hex
from dotenv import load_dotenv
from modules.get_chain_and_rpc import rpc, chain

load_dotenv()

web3 = Web3(Web3.HTTPProvider(rpc))

wallet = os.getenv('PRIVATE_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

def get_tokens_amount_for_swap():
    
amount = 100000000000000
from_token_address = '0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3'
to_token_address = '0x3ee2200efb3400fabb9aacf31297cbdd1d435d47'

swap_params_api = {
    'fromTokenAddress': web3.to_checksum_address(from_token_address),
    'toTokenAddress': web3.to_checksum_address(to_token_address),
    'amount': int(amount),
    'fromAddress': wallet,
    'slippage': 3,
}

api_base_url = f'https://api.1inch.io/v5.0/{chain}'
broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain}/broadcast'

def api_request_url( method_name, query_params):
        return f'{api_base_url}{method_name}?{urlencode(query_params)}'


def check_allowance():
    query_params = {
        'tokenAddress': swap_params_api['fromTokenAddress'],
        'walletAddress': wallet
    }
    url = api_request_url('/approve/allowance', query_params)
    responce = requests.get(url)
    allowance = responce.json()
    
    return allowance


def build_approve_transaction():
    query_params = {
        'tokenAddress': swap_params_api['fromTokenAddress'],
        'amount': 115792089237316195423570985008687907853269984665640564039457
    }

    url = api_request_url('/approve/transaction', query_params)
    response = requests.get(url)
    transaction_data = response.json()
    transaction_data['to'] = web3.to_checksum_address(transaction_data['to'])
    transaction_data['value'] = int(transaction_data['value'])
    transaction_data['gasPrice'] = int(web3.to_wei(1.5, 'gwei'))
    transaction_data['gas'] = int(250000)
    transaction_data['chainId'] = int(chain)
    transaction_data['nonce'] = web3.eth.get_transaction_count(wallet)

    return sign_and_send_transaction(transaction_data)


def sign_and_send_transaction(transaction):
    sign_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx = sign_transaction.rawTransaction
    tx = {'rawTransaction': tx.hex()}
    return broadcast_raw_transaction(tx)


def build_swap_transaction():
    url = api_request_url('/swap', query_params=swap_params_api)

    response = requests.get(url)
    transaction_data = response.json()
    transaction_data = transaction_data['tx']

    transaction_data['from'] = web3.to_checksum_address(wallet)
    transaction_data['to'] = web3.to_checksum_address(transaction_data['to'])
    transaction_data['value'] = int(transaction_data['value'])
    transaction_data['gasPrice'] = int(web3.to_wei(1.5, 'gwei'))
    transaction_data['gas'] = int(transaction_data['gas'] * 1.25)
    transaction_data['chainId'] = int(chain)
    transaction_data['nonce'] = web3.eth.get_transaction_count(wallet)
    
    print(transaction_data)
    
    return sign_and_send_transaction(transaction_data)


def broadcast_raw_transaction(tx):
    timeout = 360
    data = web3.to_json(tx)
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(broadcast_api_url, data=data, headers=headers)
    tx_hash = json.loads(response.text)
    tx_hash = tx_hash['transactionHash']
    print(tx_hash)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
    print('Transaction succsessfuly, hash is: ', tx_hash)

    return receipt, tx_hash
    

def main():
    check_token_allowance = check_allowance()
    if check_token_allowance['allowance'] == '0':
        build_approve_transaction()   
    else:
        swap_transaction = build_swap_transaction()