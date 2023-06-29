from get_inputs import *
from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

api_1inch = 'https://api.1inch.io/v5.0/'
wallet = os.getenv('PRIVATE_ADDRESS')
wallet_private = os.getenv('PRIVATE_KEY')
chain, rpc = get_inputs()
converter_private = os.getenv('COINMARKET_PRIVATE')

web3 = Web3(Web3.HTTPProvider(rpc))
