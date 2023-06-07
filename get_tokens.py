import requests

from get_names_network_tokens import network, start_token, end_token

if network == 'Ethereum':
    network == 1
if network == 'BNB Chain':
    network == 56
if network == 'Polygon':
    network == 137
if network == 'Optimism':
    network == 10
if network == 'Arbitrum':
    network == 42161
if network == 'Gnosis':
    network == 100
if network == 'Avalanche':
    network == 43114
if network == 'Fantom':
    network == 250
if network == 'Klaytn':
    network == 8217
if network == 'Aurora':
    network == 1313161554
if network == 'ZKSync Era':
    network == 324


def get_token_addresses(network, start_token, end_token):
    url = 'https://api.1inch.io/v5.0/{}/tokens'.format(network)
    response = requests.get(url)
    data = response.json()

    token_addresses = []
    for token in data:
        if token['name'] == start_token or token['name'] == end_token:
            token_addresses.append(token['address'])

    return token_addresses


addresses = get_token_addresses(network, start_token, end_token)
print("Token Addresses:")
