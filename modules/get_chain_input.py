def user_chain_input():
    user_input = input('Choose the network`s chain: ')  
    correct_user_input = check_chain_input(user_input)
    return correct_user_input

def check_chain_input(user_input):
    while True:
        valid_chains = ['ethereum', 'bnb', 'polygon', 'optimism', 'arbitrum',
                        'gnosis', 'avalanche', 'fantom', 'klaytn', 'aurora', 'zksync era']
        if user_input not in valid_chains:
            print("Invalid chain. Please try again.")
            user_input = user_chain_input()
        return user_input