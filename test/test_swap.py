def check_allowance():
    query_params = {
        'tokenAddress': swap_params_api['fromTokenAddress'],
        'walletAddress': wallet
    }
    url = api_request_url('/approve/allowance', query_params)
    responce = requests.get(url)
    allowance = responce.json()

    return allowance


def build_approve_transaction():
    query_params = {
        'tokenAddress': swap_params_api['fromTokenAddress'],
        'amount': 115792089237316195423570985008687907853269984665640564039457
    }

    url = api_request_url('/approve/transaction', query_params)
    response = requests.get(url)
    approve_transaction_data = response.json()
    approve_transaction_data['gasPrice'] = web3.to_wei(1.5, 'gwei')

    return approve_transaction_data