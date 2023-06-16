import requests
import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
private_key = os.getenv('PRIVATE_KEY')
rpc_url = os.getenv('RPC_URL')
private_address = os.getenv('PRIVATE_ADDRESS')

web3 = Web3(Web3.HTTPProvider(rpc_url))

if web3.is_connected():
    print("Успешное подключение к Ethereum-сети")
else:
    print("Ошибка подключения к Ethereum-сети")


def get_contract():
    url = 'https://api.1inch.io/v5.0/56/swap'

    params = {
        "fromTokenAddress": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # BNB token address
        "toTokenAddress": "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3",  # DAI token address
        "amount": 0.001,  # Amount of BNB to swap
        "fromAddress": private_address,  # Your wallet address
        "slippage": 1,
        "disableEstimate": True,
        "burnChi": False,
        "allowPartialFill": False
    }
    response = requests.get(url, params=params)
    response_data = response.json()
    print(response_data)
#     to_token_amount = response_data['toTokenAmount']
#     from_token_address = response_data['fromToken']['address']
#     to_token_address = response_data['toToken']['address']

#     tx_to = Web3.to_checksum_address(response_data['tx']['to'])

#     sender_address = response_data['tx']['from']
#     nonce = web3.eth.get_transaction_count(sender_address)

#     with open('erc20.abi.json') as f:
#         abi = json.load(f)
#     token_contract = web3.eth.contract(address=tx_to, abi=abi)

#     swap_tx = token_contract.functions.transfer(
#         Web3.to_checksum_address(to_token_address),
#         to_token_amount
#     ).build_transaction({
#         'from': sender_address,
#         'nonce': nonce,
#         'value': 0,
#         'gas': 1000000,
#         'gasPrice': 100000000
#     })

#     swap_signed_tx = web3.eth.account.sign_transaction(
#         swap_tx, private_key=private_key)
#     swap_tx_hash = web3.eth.send_raw_transaction(
#         swap_signed_tx.rawTransaction)
#     web3.eth.wait_for_transaction_receipt(swap_tx_hash)

#     receipt = web3.eth.wait_for_transaction_receipt(swap_tx_hash)
#     print("Транзакция успешно выполнена")
#     print("Receipt:", receipt)


get_contract()
