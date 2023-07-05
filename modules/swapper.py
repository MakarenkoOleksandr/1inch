import json
import requests
import os
from web3 import Web3
from urllib.parse import urlencode
from eth_utils import to_hex
from dotenv import load_dotenv
from modules.get_chain_and_rpc import rpc, chain

load_dotenv()

class SwapManager:
    def __init__(self):
        self.api_base_url = f'https://api.1inch.io/v5.0/{chain}'
        self.broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain}/broadcast'
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.wallet = os.getenv('PRIVATE_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.swap_params = {}

    def set_swap_params(self):
        from_tokens = input('Какой токен меняем? ').replace(',', ' ').upper()
        to_tokens = input('На какой меняем? ').replace(',', ' ').upper()
        amount = 100000000000000

        with open('./json_files/tokens.json') as f:
            tokens = json.load(f)

        for token in tokens:
            if token['symbol'] in from_tokens:
                from_token_address = token['address']
            if to_tokens == token['symbol']:
                to_token_address = token['address']

        self.swap_params = {
            'fromTokenAddress': from_token_address,
            'toTokenAddress': to_token_address,
            'amount': amount,
            'value': '0',
            'fromAddress': self.wallet,
            'slippage': 1,
            'disableEstimate': False,
            'allowPartialFill': False,
        }

    def api_request_url(self, method_name, query_params):
        return f'{self.api_base_url}{method_name}?{urlencode(query_params)}'

    async def build_approve_transaction(self):
        query_params = {
            'tokenAddress': self.swap_params['fromTokenAddress'],
            'amount': self.swap_params['amount']
        }

        url = self.api_request_url('/approve/transaction', query_params)
        response = requests.get(url)
        approve_transaction_data = response.json()
        approve_transaction_data['gasPrice'] = self.web3.to_wei(1.5, 'gwei')
        approve_transaction_data['gas'] = 25000
        return approve_transaction_data

    async def build_swap_transaction(self, amount):
        url = self.api_request_url('/swap', query_params=self.swap_params)
        response = requests.get(url)
        swap_transaction_data = response.json()
        swap_transaction_data = {
            'from': self.web3.to_checksum_address(self.wallet),
            'to': self.web3.to_checksum_address(swap_transaction_data['tx']['to']),
            'data': swap_transaction_data['tx']['data'],
            'value': self.web3.to_wei(amount, 'wei'),
            'gas': swap_transaction_data['tx']['gas'],
            'gasPrice': self.web3.to_wei(1.5, 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.wallet)
        }
        return swap_transaction_data

    async def broadcast_raw_transaction(self, raw_transaction):
        payload = {
            'rawTransaction': raw_transaction,
        }
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(
            self.broadcast_api_url, json=payload, headers=headers)
        response_data = response.json()
        transaction_hash = response_data.get('transactionHash')

        return transaction_hash

    async def sign_and_send_transaction(self, transaction):
        raw_transaction = self.web3.eth.account.sign_transaction(
            transaction, self.private_key).rawTransaction
        raw_transaction_str = to_hex(raw_transaction)
        return await self.broadcast_raw_transaction(raw_transaction_str)

    async def main(self):
        self.set_swap_params()
        sign_transaction = await self.build_approve_transaction()
        print('Transaction for approve:', sign_transaction)
        swap_transaction = await self.build_swap_transaction(100000000000000)
        print('Transaction for swap:', swap_transaction)

        print('Делаем обмен?')
        print('Для подтверждения введите ok')
        answer = input()
        if answer == 'ok':
            try:
                swap_transaction_tx = await self.sign_and_send_transaction(swap_transaction)
                print('Обмен успешно выполнен')
                print('Transaction hash:', swap_transaction_tx)
            except:
                if swap_transaction_tx == 'None':
                    print('Во время обмена произошел сбой. Повторить транзакцию?')
                    return
        else:
            print('Вы отменили обмен')
            return False

swap_manager = SwapManager()