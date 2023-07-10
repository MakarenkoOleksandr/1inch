from web3 import Web3
import os
from dotenv import load_dotenv
import json

load_dotenv()

rpc = os.getenv('BNB_RPC_URL')

web3 = Web3(Web3.HTTPProvider(rpc))

contract_address = web3.to_checksum_address('0x1111111254eeb25477b68fb85ed929f73a960582') #1inch contract
wallet = os.getenv('PRIVATE_ADDRESS')
private = os.getenv('PRIVATE_KEY')
token_address = web3.to_checksum_address('0x55d398326f99059ff775485246999027b3197955')

with open('./json_files/erc20.json') as f:
    abi = json.load(f)

amount = 115792089237316195423570985008687907853269984665640564039457

approve_contract = web3.eth.contract(address=token_address, abi=abi)
approve_data = approve_contract.encodeABI(fn_name='approve', args=[contract_address, amount])

nonce = web3.eth.get_transaction_count(wallet)
gas_price = web3.to_wei(3, 'gwei')
gas = 60000

transaction = {
    'from': wallet,
    'nonce': nonce,
    'gasPrice': gas_price,
    'gas': gas,
    'data': approve_data,
}

signed_transaction = web3.eth.account.sign_transaction(transaction, private)
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print('Transaction hash:', transaction_hash.hex())




from_tokens = input('Какой токен меняем: ').replace(',', ' ').upper()
        # to_tokens = input('На какой меняем: ').replace(',', ' ').upper()

        # from_token_address = None
        # to_token_address = None

        # while from_token_address is None or to_token_address is None:
        #     for token in tokens:
        #         if token['symbol'] == from_tokens:
        #             from_token_address = token['address']

        #         if token['symbol'] == to_tokens:
        #             to_token_address = token['address']
        #     if from_token_address is None:
        #         print('Вы ввели неправильный токен для обмена')
        #         from_tokens = input('Введите правильный токен для обмена: ').replace(',', ' ').upper()

        #     if to_token_address is None:
        #         print('Вы ввели неправильный токен для получения')
        #         to_tokens = input('Введите правильный токен для получения: ').replace(',', ' ').upper()


        input_amount = input('Введите сумму обмена: ')
        # if float(input_amount) < 1:
        #     amount = int(Decimal(input_amount) * 10 ** 18)
        # else:
        #     amount = int(web3.to_wei(input_amount, 'ether'))