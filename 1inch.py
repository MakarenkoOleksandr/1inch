import requests
from web3 import Web3


def make_trade(from_token, to_token, amount, slippage, wallet_address, private_key):

    chainId = 1
    endpoint = 'https://api.1inch.io/v5.0/{}/tokens'.format(chainId)

    # Подключение к Ethereum сети
    w3 = Web3(Web3.HTTPProvider(
        'https://mainnet.infura.io/v3/11092226beac4a518fa83083426e882f'))

    # Получение Nonce для создания транзакции
    nonce = w3.eth.get_transaction_count(wallet_address)

    # Создание объекта транзакции
    transaction = {
        'from': wallet_address,
        'to': endpoint,
        'data': {
            'fromTokenAddress': from_token,
            'toTokenAddress': to_token,
            'amount': amount,
            'fromAddress': wallet_address,
            'slippage': slippage
        },
        'nonce': nonce,
        # Пример установки цены газа
        'gasPrice': w3.toWei(100, 'gwei'),
        'gas': 300000  # Пример установки лимита газа
    }

    # Подпись транзакции с использованием приватного ключа
    signed_transaction = w3.eth.account.signTransaction(
        transaction, private_key)

    # Отправка подписанной транзакции
    response = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    if response:
        tx_hash = response.hex()
        print(
            f'Транзакция отправлена. Хеш транзакции: {tx_hash}')
    else:
        print('Произошла ошибка при выполнении обмена.')


# Пример использования функции
make_trade('0x0123456789abcdefABCDEF0123456789abcdef', '0x...', 0.0001, 1, '0x2065cc411803b37d7dc1ef31307ef066092b971e',
           '0x471746a9e3fae01b52ef4e833fc37c553db4ce5110d3a7876cb418150b3a379d')
