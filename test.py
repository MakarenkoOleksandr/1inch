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

swap_params = {
    'fromTokenAddress': '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    'toTokenAddress': '0x2170ed0880ac9a755fd29b2688956bd959f933f8',
    'amount': '1000000000000000',
    'value': '0',
    'fromAddress': wallet_address,
    'slippage': 1,
    'disableEstimate': False,
    'allowPartialFill': False,
}

broadcast_api_url = f'https://tx-gateway.1inch.io/v1.1/{chain_id}/broadcast'
api_base_url = f'https://api.1inch.io/v5.0/{chain_id}'
web3 = Web3(Web3.HTTPProvider(web3_rpc_url))


def api_request_url(method_name, query_params):
    return f'{api_base_url}{method_name}?{urlencode(query_params)}'


async def check_allowance(token_address, wallet_address):
    response = requests.get(api_request_url(
        '/approve/allowance', {'tokenAddress': token_address, 'walletAddress': wallet_address}))
    res = response.json()
    return res['allowance']


def broad_cast_raw_transaction(raw_transaction):
    response = requests.post(broadcast_api_url, json={
                             'rawTransaction': raw_transaction}, headers={'Content-Type': 'application/json'})
    res = response.json()
    return res['transactionHash']


# async def signAndSendTransaction(transaction):
#     rawTransaction = web3.eth.account.sign_transaction(
#         transaction, private_key=privateKey)['rawTransaction']
#     return await broadCastRawTransaction(rawTransaction)


# async def buildTxForApproveTradeWithRouter(tokenAddress, amount=None):
#     queryParams = {'tokenAddress': tokenAddress}
#     if amount:
#         queryParams['amount'] = amount
#     url = apiRequestUrl('/approve/transaction', queryParams)
#     response = requests.get(url)
#     transaction = response.json()
#     gasLimit = web3.eth.estimate_gas({**transaction, 'from': walletAddress})
#     transaction['gas'] = gasLimit
#     return transaction


# async def buildTxForSwap(swapParams):
#     url = apiRequestUrl('/swap', swapParams)
#     response = requests.get(url)
#     res = response.json()
#     return res['tx']


async def main():
    allowance = await check_allowance(swap_params['fromTokenAddress'], wallet_address)
    print('Allowance:', allowance)

    balance = web3.eth.get_balance(wallet_address)
    print('Account balance:', web3.from_wei(balance, 'wei'))

#     transactionForSign = await buildTxForApproveTradeWithRouter(swapParams['fromTokenAddress'], swapParams['amount'])
#     print('Transaction for approve:', transactionForSign)

#     swapTransaction = await buildTxForSwap(swapParams)
#     print('Transaction for swap:', swapTransaction)

#     ok = input(
#         'Do you want to send a transaction to exchange with 1inch router? (y/n): ')

#     if ok.lower() != 'y':
#         return False

#     swapTxHash = await signAndSendTransaction(swapTransaction)
#     print('Transaction Signed and Sent:', swapTxHash)

asyncio.run(main())
