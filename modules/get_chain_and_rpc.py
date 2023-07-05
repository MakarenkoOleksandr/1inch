import os
from dotenv import load_dotenv

load_dotenv()

eth_rpc = os.getenv('ETHERIUM_RPC_URL')
bnb_rpc = os.getenv('BNB_RPC_URL')


def user_chain_input():
    user_input = input('Choose the network`s chain: ')  
    correct_user_input = check_chain_input(user_input)
    return correct_user_input

def get_chain_and_rpc(chain_name):
    chain = True
    rpc = True
    # if chain_name == 'ethereum':
    #     chain = 1
    #     rpc = eth_rpc

    if chain_name == 'bnb':
        chain = 56
        rpc = bnb_rpc

    # if chain_name == 'polygon':
    #     chain = 137

    # if chain_name == 'optimism':
    #     chain = 10

    # if chain_name == 'arbitrum':
    #     chain = 42161

    # if chain_name == 'gnosis':
    #     chain = 100

    # if chain_name == 'avalanche':
    #     chain = 43114

    # if chain_name == 'fantom':
    #     chain = 250

    # if chain_name == 'klaytn':
    #     chain = 8217

    # if chain_name == 'aurora':
    #     chain = 1313161554

    # if chain_name == 'zksync Era':
    #     chain = 324
    return chain, rpc

def check_chain_input(user_input):
    while True:
        valid_chains = ['ethereum', 'bnb', 'polygon', 'optimism', 'arbitrum',
                        'gnosis', 'avalanche', 'fantom', 'klaytn', 'aurora', 'zksync era']
        if user_input not in valid_chains:
            print("Invalid chain. Please try again.")
            user_input = user_chain_input()
        return user_input
 
user_input = user_chain_input()
chain, rpc = get_chain_and_rpc(user_input)