from get_token_adress import get_token_address
from get_API import get_API
from get_inputs import get_inputs

network, start_token, end_token = get_inputs()
get_API(network)
get_token_address(start_token, end_token)
# python main_1inch.py --network Arbitrum --start_token Ethereum --end_token "Tether USD"
