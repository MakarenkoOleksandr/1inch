from eth_utils import encode_hex
import aiohttp
import requests
from web3 import Web3
from urllib.parse import urlencode
import os
import asyncio
import json
from eth_utils import to_hex
from dotenv import load_dotenv
load_dotenv()

chain_id = 56
web3_rpc_url = os.getenv('BNB_RPC_URL')
wallet = os.getenv('PRIVATE_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')
swap_value = 1000000000000000

swap_params = {
    'fromTokenAddress': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    'toTokenAddress': '0x2170ed0880ac9a755fd29b2688956bd959f933f8',
    'amount': swap_value,
    'value': '0',
    'fromAddress': wallet,
    'slippage': 1,
    'disableEstimate': False,
    'allowPartialFill': False,
}

api_base_url = f'https://api.1inch.io/v5.0/{chain_id}'
broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain_id}/broadcast'
web3 = Web3(Web3.HTTPProvider(web3_rpc_url))


def api_request_url(method_name, query_params):
    return f'{api_base_url}{method_name}?{urlencode(query_params)}'


async def build_approve_transaction():
    query_params = {
        'tokenAddress': swap_params['fromTokenAddress'],
        'amount': swap_value
    }

    url = api_request_url('/approve/transaction', query_params)
    responce = requests.get(url)
    approve_transaction_data = responce.json()
    approve_transaction_data['gasPrice'] = web3.to_wei(1.5, 'gwei')
    approve_transaction_data['gas'] = 25000
    return approve_transaction_data


async def build_swap_transaction(wallet_address, amount):
    url = api_request_url('/swap', query_params=swap_params)
    responce = requests.get(url)
    swap_transaction_data = responce.json()
    swap_transaction_data = {
        'from': Web3.to_checksum_address(wallet_address),
        'to': Web3.to_checksum_address(swap_transaction_data['tx']['to']),
        'data': swap_transaction_data['tx']['data'],
        'value': web3.to_wei(amount, 'wei'),
        'gas': swap_transaction_data['tx']['gas'],
        'gasPrice': web3.to_wei(1.5, 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address)
    }
    return swap_transaction_data


async def broadcast_raw_transaction(raw_transaction):
    payload = {
        'rawTransaction': raw_transaction,
    }
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(
        broadcast_api_url, json=payload, headers=headers)
    response_data = response.json()
    print(response_data)
    transaction_hash = response_data.get('transactionHash')

    return transaction_hash


async def sign_and_send_transaction(transaction):
    raw_transaction = web3.eth.account.sign_transaction(
        transaction, private_key).rawTransaction
    raw_transaction_str = to_hex(raw_transaction)
    return await broadcast_raw_transaction(raw_transaction_str)


async def main():
    sign_transaction = await build_approve_transaction()
    print('Transaction for approve:', sign_transaction)
    swap_transaction = await build_swap_transaction(wallet, swap_value)
    print('Transaction for swap:', swap_transaction)
    swap_transaction_tx = await sign_and_send_transaction(swap_transaction)
asyncio.run(main())
