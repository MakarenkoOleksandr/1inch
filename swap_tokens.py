import requests
from dotenv import load_dotenv

load_dotenv()


def swap_tokens(s_a, e_a, w_a, a, n):
    url = 'https://api.1inch.io/v5.0/{}/swap'.format(n)

    params = {
        'fromTokenAddress': s_a,
        'toTokenAddress': e_a,
        'amount': a,
        'fromAddress': w_a,
        'slippage': 1
    }

    response = requests.get(url, json=params)
    result = response.json()
    print(result)
    # # Обрабатываем ответ
    # if response.status_code == 200:
    #     result = response.json()
    #     if 'toTokenAmount' in result:
    #         to_token_amount = result['toTokenAmount']
    #         print(
    #             f"Успешно! Получено {to_token_amount / 10 ** 18} {to_token_address}")
    #     else:
    #         print('Что-то пошло не так при обмене.')
    # else:
    #     print('Ошибка при отправке запроса.', response.text)
