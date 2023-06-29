from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Session
from decimal import Decimal, ROUND_HALF_UP
import json

with open('./json_files/tokens.json') as f:
    tokens = json.load(f)

amount = 1

token_prices = []

for token in tokens:
    symbol = token['symbol']

    def get_prices(amount, token_symbol):
        url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

        parameters = {
            'amount': amount,
            'symbol': token_symbol
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '1159ece7-4e94-429c-8eb8-e52bd27beec4',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = response.json()
            price = Decimal(data['data'][0]['quote']['USD']['price'])

            # token_prices.append({
            #     'symbol': token_symbol,
            #     'price': str(price)
            # })
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        # balance_in_usd = price.quantize(
        #     Decimal('0.00'), rounding=ROUND_HALF_UP)
        # print(
        #     f"Баланс токена {token_name}: {token_balance} ~ {balance_in_usd} $")
        with open('./json_files/token_prices.json', 'w') as f:
            json.dump(token_prices, f, indent=4)
    get_prices(amount, symbol)
