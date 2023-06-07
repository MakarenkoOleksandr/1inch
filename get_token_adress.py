import json


def get_token_address(s_t, e_t):
    with open('tokens_data.json') as file:
        data = json.load(file)
        tokens = data['tokens']
        start_address = None
        end_address = None
        for token in tokens.values():
            if token.get('name') == s_t:
                start_address = token.get('address')
            elif token.get('name') == e_t:
                end_address = token.get('address')
            if start_address and end_address:
                break
    print(start_address, end_address)
    return start_address, end_address
