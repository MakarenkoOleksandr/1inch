import os
import json
from decimal import Decimal, ROUND_HALF_UP
from dotenv import load_dotenv
from web3 import Web3
import aiohttp
from modules.get_chain_and_rpc import rpc
import time

load_dotenv()


class TokenBalanceChecker:
    def __init__(self):
        self.rpc = rpc
        self.wallet = os.getenv('PRIVATE_ADDRESS')
        self.wallet_private = os.getenv('PRIVATE_KEY')
        self.converter_private = os.getenv('COINMARKET_PRIVATE')
        self.tokens = None
        self.token_abi = None
        self.web3 = None
        with open('./json_files/tokens.json') as tokens_file:
            self.tokens = json.load(tokens_file)

        with open('./json_files/erc20.json') as abi_file:
            self.token_abi = json.load(abi_file)

    async def get_balance(self, token, wallet):
        token_contract = self.web3.eth.contract(
            address=self.web3.to_checksum_address(token), abi=self.token_abi)
        balance = token_contract.functions.balanceOf(wallet).call()

        return balance

    async def convert_to_usd(self, token_symbol, token_balance):

        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

        parameters = {
            'amount': str(token_balance),
            'symbol': token_symbol
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.converter_private,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=parameters, headers=headers) as response:
                    data = await response.json()
                    price = Decimal(data['data'][0]['quote']['USD']['price'])
            except aiohttp.ClientError as e:
                print(e)

        balance_in_usd = price.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        print(f"Token balance for {token_symbol}: ~ {token_balance} ~ {balance_in_usd} $")

    async def get_tokens_balance(self):
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        native_token_balance = self.web3.eth.get_balance(self.wallet)
        native_token_balance = self.web3.from_wei(native_token_balance, 'ether')

        for token in self.tokens:
            if token['address'] == '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                await self.convert_to_usd(self.tokens[0]['symbol'], native_token_balance)
            else:
                token_balance = await self.get_balance(token['address'], self.wallet)
                if token_balance > 0:
                    token_balance = self.web3.from_wei(token_balance, 'ether')
                    await self.convert_to_usd(token['symbol'], token_balance)


async def main():
    start_time = time.time()
    
    balance_checker = TokenBalanceChecker()
    await balance_checker.get_tokens_balance()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Скрипт выполнен за", execution_time, "секунд.")