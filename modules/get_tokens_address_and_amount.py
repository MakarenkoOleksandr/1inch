import json
from decimal import Decimal
from web3 import Web3
import os
from dotenv import load_dotenv
from modules.get_chain_and_rpc import rpc

load_dotenv()

web3 = Web3(Web3.HTTPProvider(rpc))
wallet = os.getenv('PRIVATE_ADDRESS')

with open('./json_files/erc20.json') as abi_file:
    token_abi = json.load(abi_file)
with open('./json_files/tokens.json') as f:
        tokens = json.load(f)
   

def get_from_tokens_input():
    from_token_input = input('Token to send: ').replace(',', ' ').upper()
    correct_from_token_input = check_from_tokens_input(from_token_input)
    return correct_from_token_input


def check_from_tokens_input(token_input):
    for token in tokens:
        if token_input == token['symbol']:
            token_address = token['address']
            return token_address
        
    print('Warning! You have entered a wrong send token. Try again: ')
    return get_from_tokens_input()


def get_to_tokens_input():
    to_token_input = input('Token to receive: ').replace(',', ' ').upper()
    correct_to_token_input = check_to_tokens_input(to_token_input)
    return correct_to_token_input


def check_to_tokens_input(token_input):
    for token in tokens:
        if token_input == token['symbol']:
            token_address = token['address']
            return token_address

    print('Warning! You have enter wrong receive token. Try again: ')
    token_address = get_to_tokens_input()

def get_amount_input(from_token_address):
    input_amount = input('Enter amount for swap: ')
    correct_input_amount = check_amount_input(input_amount, from_token_address)
    return correct_input_amount

def check_amount_input(input_amount, from_token_address):
    while input_amount != 'max':
        try:
            amount = float(input_amount)
            if 0 < amount < 1:
                amount = int(Decimal(input_amount) * 10 ** 18)
                break
            elif amount >= 1:
                amount = int(web3.to_wei(input_amount, 'ether'))
                break
        except ValueError:
            print('Value must be a number. Try again')
        
        get_amount_input()

    if input_amount == 'max':
        token_contract = web3.eth.contract(address=web3.to_checksum_address(from_token_address), abi=token_abi)
        balance = token_contract.functions.balanceOf(wallet).call()
        amount = balance

    return amount


def get_tokens_address_and_amount_for_swap():
    from_token_address = get_from_tokens_input()
    to_token_address = get_to_tokens_input()                 
    amount = get_amount_input(from_token_address)

    return from_token_address, to_token_address, amount