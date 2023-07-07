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

class SwapManager:


    def __init__(self):
        self.api_base_url = f'https://api.1inch.io/v5.0/{chain}'
        self.broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain}/broadcast'
        self.web3 = Web3(Web3.HTTPProvider(rpc))
        self.wallet = os.getenv('PRIVATE_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.swap_params = {}

        with open('./json_files/tokens.json') as f:
            self.tokens = json.load(f)


    def set_swap_params(self):
        from_tokens = input('Какой токен меняем: ').replace(',', ' ').upper()
        to_tokens = input('На какой меняем: ').replace(',', ' ').upper()

        self.from_token_address = None
        self.to_token_address = None

        #Нужно вынести в отдельную функцию проверку инпутов
        while self.from_token_address is None or self.to_token_address is None:
            for token in self.tokens:
                if token['symbol'] == from_tokens:
                    self.from_token_address = token['address']

                if token['symbol'] == to_tokens:
                    self.to_token_address = token['address']
            if self.from_token_address is None:
                print('Вы ввели неправильный токен для обмена')
                from_tokens = input('Введите правильный токен для обмена: ').replace(',', ' ').upper()

            if self.to_token_address is None:
                print('Вы ввели неправильный токен для получения')
                to_tokens = input('Введите правильный токен для получения: ').replace(',', ' ').upper()

        input_amount = input('Введите сумму обмена: ')
        if float(input_amount) < 1:
            self.amount = int(Decimal(input_amount) * 10 ** 18)
        else:
            self.amount = int(self.web3.to_wei(input_amount, 'ether'))

        self.swap_params = {
            'fromTokenAddress': self.from_token_address,
            'toTokenAddress': self.to_token_address,
            'amount': self.amount,
            'value': '0',
            'fromAddress': self.wallet,
            'slippage': 1,
            'disableEstimate': False,
            'allowPartialFill': False,
        }


    def api_request_url(self, method_name, query_params):
        return f'{self.api_base_url}{method_name}?{urlencode(query_params)}'


    async def check_allowance(self):
        query_params = {
            'tokenAddress': self.swap_params['fromTokenAddress'],
            'walletAddress': self.wallet
        }
        url = self.api_request_url('/approve/allowance', query_params)
        responce = requests.get(url)
        allowance = responce.json()

        return allowance


    async def build_approve_transaction(self):
        query_params = {
            'tokenAddress': self.swap_params['fromTokenAddress'],
            'amount': self.swap_params['amount']
        }

        url = self.api_request_url('/approve/transaction', query_params)
        response = requests.get(url)
        approve_transaction_data = response.json()
        approve_transaction_data['gasPrice'] = self.web3.to_wei(1.5, 'gwei')
        approve_transaction_data['gas'] = self.web3.eth.gas_price
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
        
        if transaction_hash is None:
            raise ValueError('Transaction hash is missing in the response.')
        
        return transaction_hash


    async def sign_and_send_transaction(self, transaction):
        raw_transaction = self.web3.eth.account.sign_transaction(
            transaction, self.private_key).rawTransaction
        raw_transaction_str = to_hex(raw_transaction)
        return await self.broadcast_raw_transaction(raw_transaction_str)


    async def main(self):
        self.set_swap_params()

        allowance = await self.check_allowance()
        print('Allowance: ', allowance)
        if int(allowance['allowance']) == 0:
            print('Your allowance is low. Need get approval')
            try:
                approve_transaction = await self.build_approve_allowance()
                print('Transaction for approval:', approve_transaction)

                approve_transaction_tx = await self.sign_and_send_transaction(approve_transaction)
                print('Transaction hash:', approve_transaction_tx)
            except:
                print('Failed to build approval transaction.')


        swap_transaction = await self.build_swap_transaction(self.amount)
        print('Transaction for swap:', swap_transaction)

        print('Делаем обмен?')
        answer = input('Для подтверждения введите "ok": ')
        if answer == 'ok':
            while True:
                try:
                    swap_transaction_tx = await self.sign_and_send_transaction(swap_transaction)
                    print('Обмен успешно выполнен')
                    print('Transaction hash:', swap_transaction_tx)
                    break  # Выходим из цикла после успешного обмена
                except:
                    answer = input('Во время обмена произошел сбой. Повторить транзакцию? (Введите "ok" для повтора) ')
                    if answer != 'ok':
                        print('Вы отменили обмен')
                        return False
        else:
            print('Вы отменили обмен')
            return False

swap_manager = SwapManager()
