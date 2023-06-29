import argparse
from dotenv import load_dotenv
import os

load_dotenv()
eth_rpc = os.getenv('ETHERIUM_RPC_URL')
bnb_rpc = os.getenv('BNB_RPC_URL')


def get_inputs():

    parser = argparse.ArgumentParser(description="Exchange token script")
    parser.add_argument("--chain", required=True, help="Network name")

    args = parser.parse_args()

    input_chain = args.chain

    if input_chain == 'Ethereum':
        input_chain = 1
        rpc_url = eth_rpc

    if input_chain == 'BNB':
        input_chain = 56
        rpc_url = bnb_rpc

    if input_chain == 'Polygon':
        input_chain = 137

    if input_chain == 'Optimism':
        input_chain = 10

    if input_chain == 'Arbitrum':
        input_chain = 42161

    if input_chain == 'Gnosis':
        input_chain = 100

    if input_chain == 'Avalanche':
        input_chain = 43114

    if input_chain == 'Fantom':
        input_chain = 250

    if input_chain == 'Klaytn':
        input_chain = 8217

    if input_chain == 'Aurora':
        input_chain = 1313161554

    if input_chain == 'ZKSync Era':
        input_chain = 324

    return input_chain, rpc_url
