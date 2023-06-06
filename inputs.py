import argparse

# Создаем парсер аргументов командной строки
parser = argparse.ArgumentParser(description="Exchange token script")
parser.add_argument("--network", required=True, help="Network name")
parser.add_argument("--start_token", required=True, help="Start token")
parser.add_argument("--end_token", required=True, help="End token")

# Разбираем аргументы командной строки
args = parser.parse_args()

# Получаем значения аргументов
network = args.network
start_token = args.start_token
end_token = args.end_token


# Пример вывода полученных значений
print("Network:", network)
print("Start token:", start_token)
print("End token:", end_token)

# Запуск скрипта
# python inputs.py --network Arbitrum --start_token Ethereum --end_token "Tether USD"
