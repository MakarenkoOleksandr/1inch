import os
from get_inputs import *
from get_token_adress import *
from dotenv import load_dotenv
from swap_tokens import *

load_dotenv()
wallet_address = os.getenv('PRIVATE_ADDRESS')

network, start_token, end_token, amount = get_inputs()
get_tokens_API(network)
start_address, end_address = get_token_address(start_token, end_token)
# swap_tokens()
swap_tokens(start_address, end_address, wallet_address, amount)
print(amount)
# python main_1inch.py --network Arbitrum --start_token "Tether USD" --end_token Ethereum --amount 1
