import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from web3 import Web3
import json

load_dotenv()

rpc = os.getenv('BNB_RPC_URL')
wallet = os.getenv('PRIVATE_ADDRESS')
private = os.getenv('PRIVATE_KEY')
api_base_url = f'https://api.1inch.io/v5.0/56'
broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/56/broadcast'
token_to_approve = '0x3ee2200efb3400fabb9aacf31297cbdd1d435d47'
chain = 56

web3 = Web3(Web3.HTTPProvider(rpc))

def api_request_url( method_name, query_params):
        return f'{api_base_url}{method_name}?{urlencode(query_params)}'

def check_allowance():
    query_params = {
        'tokenAddress': token_to_approve,
        'walletAddress': wallet
    }
    url = api_request_url('/approve/allowance', query_params)
    responce = requests.get(url)
    allowance = responce.json()
    print(allowance)
    if allowance['allowance'] == '0':
        build_approve_transaction()
        return allowance
    else:
        return allowance


def build_approve_transaction():
    query_params = {
        'tokenAddress': token_to_approve,
        'amount': int(115792089237316195423570985008687907853269984665640564039457)
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
    


# def sign_and_send_transaction(transaction):
#     sign_transaction = web3.eth.account.sign_transaction(transaction, private)
#     tx = sign_transaction.rawTransaction
#     tx = {'rawTransaction': tx.hex()}
#     return broadcast_raw_transaction(tx)

allowance = check_allowance()
print(allowance)