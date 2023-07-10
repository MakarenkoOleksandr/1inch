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
    approve_transaction_data = response.json()
    approve_transaction_data['gasPrice'] = web3.to_wei(1.5, 'gwei')

    return approve_transaction_data


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
    


def sign_and_send_transaction(transaction):
    sign_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx = sign_transaction.rawTransaction
    tx = {'rawTransaction': tx.hex()}
    return broadcast_raw_transaction(tx)


def build_swap_transaction():
    url = api_request_url('/swap', query_params=swap_params_api)

    response = requests.get(url)
    swap_transaction_data = response.json()
    swap_transaction_data = swap_transaction_data['tx']

    swap_transaction_data['from'] = web3.to_checksum_address(wallet)
    swap_transaction_data['to'] = web3.to_checksum_address(swap_transaction_data['to'])
    swap_transaction_data['value'] = int(swap_transaction_data['value'])
    swap_transaction_data['gasPrice'] = int(web3.to_wei(1.5, 'gwei'))
    swap_transaction_data['gas'] = int(swap_transaction_data['gas'] * 1.25)
    swap_transaction_data['chainId'] = int(chain)
    swap_transaction_data['nonce'] = web3.eth.get_transaction_count(wallet)
    
    print(swap_transaction_data)
    
    return sign_and_send_transaction(swap_transaction_data)


def main():
        # swap_manager.set_swap_params()

        # allowance = await swap_manager.check_allowance()
        # print('Allowance: ', allowance)
        # if int(allowance['allowance']) == 0:
        #     print('Your allowance is low. Need get approval')
            
        #     approve_transaction = await swap_manager.build_approve_transaction()
        #     print('Transaction for approval:', approve_transaction)
            
        #     while True:
        #         try:
        #             approve_transaction_tx = await swap_manager.sign_and_send_transaction(approve_transaction)
        #             print('Transaction hash:', approve_transaction_tx)
        #             break
        #         except:
        #             answer = input('Во время подтверждения токена произошел сбой. Повторить транзакцию? (Введите "ok" для повтора) ')
        #             if answer != 'ok':
        #                 print('Вы отменили обмен')
        #                 return False
        # else:
        #     print('Failed to build approval transaction.')


    swap_transaction = build_swap_transaction()
    

                    

