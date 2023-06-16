import requests
import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv('PRIVATE_KEY')
rpc_url = os.getenv('RPC_URL')

web3 = Web3(Web3.HTTPProvider(rpc_url))

if web3.is_connected():
    print("Успешное подключение к Ethereum-сети")
else:
    print("Ошибка подключения к Ethereum-сети")


def get_contract():
    url = 'https://api.1inch.io/v5.0/42161/swap?fromTokenAddress=0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9&toTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&amount=1&fromAddress=0xb2D7032421e1ff894b14Dc9384A7Cc2Cc312e5AD&slippage=1&disableEstimate=true&burnChi=false&allowPartialFill=false'

    response = requests.get(url)
    response_data = response.json()

    from_token_amount = response_data['fromTokenAmount']
    from_token_address = response_data['fromToken']['address']
    to_token_address = response_data['toToken']['address']

    tx_to = Web3.to_checksum_address(response_data['tx']['to'])

    sender_address = response_data['tx']['from']
    nonce = web3.eth.get_transaction_count(sender_address)

    with open('erc20.abi.json') as f:
        abi = json.load(f)
    token_contract = web3.eth.contract(address=tx_to, abi=abi)

    approve_tx = token_contract.functions.transferFrom(from_token_address, to_token_address, sender_address, from_token_amount).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'value': 1,
        'gas': 1000000,
        'gasPrice': 100000000
    })

    approve_signed_tx = web3.eth.account.sign_transaction(
        approve_tx, private_key=private_key)
    approve_tx_hash = web3.eth.send_raw_transaction(
        approve_signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(approve_tx_hash)

    receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)
    print("Транзакция успешно выполнена")
    print("Receipt:", receipt)


get_contract()
