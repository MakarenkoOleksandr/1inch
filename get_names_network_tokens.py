import argparse
import requests
import json

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="Exchange token script")
parser.add_argument("--network", required=True, help="Network name")
parser.add_argument("--start_token", required=True, help="Start token")
parser.add_argument("--end_token", required=True, help="End token")

# Разбираем аргументы командной строки
args = parser.parse_args()

# Получаем значения аргументов
network = args.network
start_token = args.start_token
end_token = args.end_token

if network == 'Ethereum':
    network = 1
if network == 'BNB Chain':
    network = 56
if network == 'Polygon':
    network = 137
if network == 'Optimism':
    network = 10
if network == 'Arbitrum':
    network = 42161
if network == 'Gnosis':
    network = 100
if network == 'Avalanche':
    network = 43114
if network == 'Fantom':
    network = 250
if network == 'Klaytn':
    network = 8217
if network == 'Aurora':
    network = 1313161554
if network == 'ZKSync Era':
    network = 324


def get_token_addresses(n):
    url = 'https://api.1inch.io/v5.0/{}/tokens'.format(n)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Открываем файл для записи
        with open('tokens_data.json', 'w') as file:
            # Записываем данные в JSON-файл
            json.dump(data, file)

        print("Данные успешно сохранены в файл 'token_addresses.json'")
    else:
        print("Ошибка при получении данных")


get_token_addresses(network)


def get_token_address(n, n_):
    with open('tokens_data.json') as file:
        data = json.load(file)
        tokens = data['tokens']
        start_address = None
        end_address = None
        for token in tokens.values():
            if token.get('name') == n:
                start_address = token.get('address')
            elif token.get('name') == n_:
                end_address = token.get('address')
            if start_address and end_address:
                break
    print(start_address, end_address)
    return start_address, end_address


get_token_address(start_token, end_token)

# Запуск скрипта
# python get_names_network_tokens.py --network Arbitrum --start_token Ethereum --end_token "Tether USD"
