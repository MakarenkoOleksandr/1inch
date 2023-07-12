import json
import requests
from decimal import Decimal
import os
from web3 import Web3
from urllib.parse import urlencode
from eth_utils import to_hex
from dotenv import load_dotenv
from modules.get_chain_and_rpc import rpc, chain
from modules.get_tokens_address_and_amount import get_tokens_address_and_amount_for_swap

load_dotenv()

class SwapManager():
    def __init__(self):
        self.rpc = rpc
        self.chain = chain
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        self.wallet = os.getenv('PRIVATE_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.api_base_url = f'https://api.1inch.io/v5.0/{chain}'
        self.broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain}/broadcast'
        self.from_token_address = None
        self.to_token_address = None
        self.amount = None
        self.swap_params_api = {}
        
    def swap_params(self):
        self.from_token_address, self.to_token_address, self.amount = get_tokens_address_and_amount_for_swap()
        self.swap_params_api = {
            'fromTokenAddress': self.web3.to_checksum_address(self.from_token_address),
            'toTokenAddress': self.web3.to_checksum_address(self.to_token_address),
            'amount': int(self.amount),
            'fromAddress': self.wallet,
            'slippage': 3,
        }
        return self.from_token_address, self.to_token_address, self.amount


    def api_request_url(self, method_name, query_params):
        return f'{self.api_base_url}{method_name}?{urlencode(query_params)}'


    def check_allowance(self):
        query_params = {
            'tokenAddress': self.from_token_address,
            'walletAddress': self.wallet
        }
        url = self.api_request_url('/approve/allowance', query_params)
        responce = requests.get(url)
        allowance = responce.json()
        return allowance['allowance']


    def build_approve_transaction(self):
        query_params = {
            'tokenAddress': self.from_token_address,
            'amount': 115792089237316195423570985008687907853269984665640564039457
        }

        url = self.api_request_url('/approve/transaction', query_params)
        response = requests.get(url)
        transaction_data = response.json()
        transaction_data['to'] = self.web3.to_checksum_address(transaction_data['to'])
        transaction_data['value'] = int(transaction_data['value'])
        transaction_data['gasPrice'] = int(self.web3.to_wei(1.5, 'gwei'))
        transaction_data['gas'] = int(250000)
        transaction_data['chainId'] = int(chain)
        transaction_data['nonce'] = self.web3.eth.get_transaction_count(self.wallet)

        return transaction_data
    

    def build_swap_transaction(self):
        url = self.api_request_url('/swap', query_params=self.swap_params_api)

        response = requests.get(url)
        transaction_data = response.json()
        transaction_data = transaction_data['tx']

        transaction_data['from'] = self.web3.to_checksum_address(self.wallet)
        transaction_data['to'] = self.web3.to_checksum_address(transaction_data['to'])
        transaction_data['value'] = int(transaction_data['value'])
        transaction_data['gasPrice'] = int(self.web3.to_wei(1.5, 'gwei'))
        transaction_data['gas'] = int(transaction_data['gas'] * 1.25)
        transaction_data['chainId'] = int(chain)
        transaction_data['nonce'] = self.web3.eth.get_transaction_count(self.wallet)
        
        return transaction_data

    def sign_and_send_transaction(self, transaction):
        sign_transaction = self.web3.eth.account.sign_transaction(transaction, self.private_key)
        tx = sign_transaction.rawTransaction
        tx = {'rawTransaction': tx.hex()}
        return tx
    

    def broadcast_raw_transaction(self, tx):
        timeout = 360
        data = self.web3.to_json(tx)
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(self.broadcast_api_url, data=data, headers=headers)
        tx_hash = json.loads(response.text)
        tx_hash = tx_hash['transactionHash']
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)

        return tx_hash
    

    def main():
        swap_manager.swap_params()
        check_token_allowance = swap_manager.check_allowance()
        print(f'You can spend: {check_token_allowance} wei')
        if check_token_allowance != '0':
            print('Your allowance is ok. Running swap transaction')
        else:
            print('Your allowance is not enough for operating. Running approve transaction')
            allowance_transaction = swap_manager.build_approve_transaction()
            signed_allowance_transaction = swap_manager.sign_and_send_transaction(allowance_transaction)
            tx_hash = swap_manager.broadcast_raw_transaction(signed_allowance_transaction)
            print('Allowance approved, hash of transaction is: ', tx_hash)
            print('Now your allowance is ok. Running swap transaction')
        swap_transaction = swap_manager.build_swap_transaction()
        signed_swap_transaction = swap_manager.sign_and_send_transaction(swap_transaction)
        tx_hash = swap_manager.broadcast_raw_transaction(signed_swap_transaction)
        print('Swap transaction is successfully, hash of transaction is: ', tx_hash)

swap_manager = SwapManager()