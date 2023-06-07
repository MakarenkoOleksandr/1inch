import argparse


def get_inputs():

    parser = argparse.ArgumentParser(description="Exchange token script")
    parser.add_argument("--network", required=True, help="Network name")
    parser.add_argument("--start_token", required=True, help="Start token")
    parser.add_argument("--end_token", required=True, help="End token")

    args = parser.parse_args()

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
    return network, start_token, end_token
