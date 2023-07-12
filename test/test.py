from decimal import Decimal
from web3 import Web3
import os 
from dotenv import load_dotenv
import json

load_dotenv()

rpc = os.getenv('BNB_RPC_URL')
web3 = Web3(Web3.HTTPProvider(rpc))
wallet = os.getenv('PRIVATE_ADDRESS')
from_token_address = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'

with open('./json_files/erc20.json') as abi_file:
    token_abi = json.load(abi_file)


input_amount = input('Введите сумму обмена: ')
if not input_amount.isdigit():
    print('Warning! Amount must be a number. Try again: ')
if input_amount == 'max':
    token_contract = web3.eth.contract(address=web3.to_checksum_address(from_token_address), abi=token_abi)
    balance = token_contract.functions.balanceOf(wallet).call()
    amount = balance
if input_amount != 'max':
    if float(input_amount) < 1:
        amount = int(Decimal(input_amount) * 10 ** 18)
    else:
        amount = int(web3.to_wei(input_amount, 'ether'))    