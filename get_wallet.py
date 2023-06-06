import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Функция для получения адреса кошелька и приватного ключа из гугл таблицы
def get_wallet_info():
    scope = ['https://docs.google.com/spreadsheets/d/1yuCuysUXXfBadxd7s4zsCQXR1ntVU3HoBdfnntxECeU/edit#gid=0',
             'https://www.googleapis.com/auth/drive']

    # Укажите путь к файлу JSON с учетными данными вашего сервисного аккаунта
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'path/to/service_account_credentials.json', scope)

    # Подключение к гугл таблице
    gc = gspread.authorize(credentials)
    sheet = gc.open('Название гугл таблицы').sheet1

    # Получение значения адреса кошелька и приватного ключа из ячеек A1 и B1
    wallet_address = sheet.acell('A1').value
    private_key = sheet.acell('B1').value

    return wallet_address, private_key


# Использование функции
wallet_address, private_key = get_wallet_info()