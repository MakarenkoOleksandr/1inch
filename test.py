import requests
from web3 import Web3
from urllib.parse import urlencode
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

chain_id = 56
web3_rpc_url = os.getenv('BNB_RPC_URL')
wallet_address = os.getenv('PRIVATE_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')
amount = 1000000000000000

swap_params = {
    'fromTokenAddress': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    'toTokenAddress': '0x2170ed0880ac9a755fd29b2688956bd959f933f8',
    'amount': amount,
    'value': '0',
    'fromAddress': Web3.to_checksum_address(wallet_address),
    'slippage': 1,
    'disableEstimate': False,
    'allowPartialFill': False,
}

broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain_id}/broadcast'
api_base_url = f'https://api.1inch.io/v5.0/{chain_id}'
web3 = Web3(Web3.HTTPProvider(web3_rpc_url))


def api_request_url(method_name, query_params):
    return f'{api_base_url}{method_name}?{urlencode(query_params)}'


async def build_tx_for_approve_trade_with_router(token_address, amount=None):
    query_params = {'tokenAddress': token_address}
    if amount:
        query_params['amount'] = amount
    url = api_request_url('/approve/transaction', query_params)
    response = requests.get(url)
    transaction = response.json()
    transaction['to'] = Web3.to_checksum_address(transaction['to'])
    gas_limit = web3.eth.estimate_gas(
        {**transaction, 'from': Web3.to_checksum_address(wallet_address)})
    transaction['gas'] = gas_limit
    return transaction


async def broad_cast_raw_transaction(raw_transaction):
    response = requests.post(broadcast_api_url, json={
                             'rawTransaction': raw_transaction}, headers={'Content-Type': 'application/json'})
    res = response.json()
    return res['transactionHash']


async def sign_and_send_transaction(transaction):
    raw_transaction = web3.eth.account.sign_transaction(
        transaction, private_key=private_key)['rawTransaction']
    return await broad_cast_raw_transaction(raw_transaction)


async def build_tx_for_swap(swapParams):
    url = api_request_url('/swap', swapParams)
    response = requests.get(url)
    res = response.json()
    res['tx']['nonce'] = web3.eth.get_transaction_count(wallet_address)
    res['tx']['to'] = Web3.to_checksum_address(res['tx']['to'])
    res['tx']['value'] = web3.to_wei(swap_params['amount'], 'wei')
    res['tx']['gasPrice'] = web3.to_wei(1.5, 'gwei')
    return res['tx']


async def main():
    transaction_for_sign = await build_tx_for_approve_trade_with_router(Web3.to_checksum_address(swap_params['fromTokenAddress']), swap_params['amount'])
    print('Transaction for approve:', transaction_for_sign)

    swap_transaction = await build_tx_for_swap(swap_params)
    print('Transaction for swap:', swap_transaction)

    ok = input(
        'Do you want to send a transaction to exchange with 1inch router? (y/n): ')

    if ok.lower() != 'y':
        return False

    swap_tx_hash = await sign_and_send_transaction(swap_transaction)
    print('Transaction Signed and Sent:', swap_tx_hash)

asyncio.run(main())
