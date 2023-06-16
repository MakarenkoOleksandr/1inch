import json
import requests


def get_tokens_API(n):
    url = 'https://api.1inch.io/v5.0/{}/tokens'.format(n)
    headers = {
        "cache-control": "public,max-age=300,s-maxage=300",
        "content-type": "application/json; charset=utf-8"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        with open('tokens_data.json', 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print("Ошибка при получении данных")


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
    return start_address, end_address
