import requests
import json


def get_API(n):
    url = 'https://api.1inch.io/v5.0/{}/tokens'.format(n)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Открываем файл для записи
        with open('tokens_data.json', 'w') as file:
            json.dump(data, file)

        print("Данные успешно сохранены в файл 'token_addresses.json'")
    else:
        print("Ошибка при получении данных")
