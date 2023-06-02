import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get("https://app.1inch.io/")
wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".header-button.header-button-smoke-blue")))


time.sleep(1)

# Выполнить клик на элемент
element.click()

# Закрыть браузер
driver.quit()

# def choose_platform(platform):
#     swap_url = "https://app.1inch.io/"


# def account_log_in():


# def swap_tokens(api_key, from_token, to_token, amount):

#     # URL для совершения обмена на сервисе 1inch
#     swap_url = "https://app.1inch.io/#/42161/simple/swap/ETH/USDT"

#     payload = {
#         "fromTokenAddress": from_token,
#         "toTokenAddress": to_token,
#         "amount": amount,
#         "fromAddress": "your_ethereum_address",
#         "slippage": 1
#     }

#     headers = {
#         "Authorization": f"Bearer {api_key}"
#     }

#     response = requests.post(swap_url, json=payload, headers=headers)

#     if response.status_code == 200:
#         swap_data = response.json()
#         # Обработка данных об обмене
#         return swap_data
#     else:
#         # Обработка ошибок
#         return None

# # Пример использования функции обмена токенов
# api_key = "your_api_key"
# from_token = "0x0000000000000000000000000000000000000000"  # Адрес токена Ethereum (ETH)
# to_token = "0x0000000000000000000000000000000000000000"  # Адрес токена Tether (USDT)
# amount = 1.0  # Количество токенов для обмена

# swap_result = swap_tokens(api_key, from_token, to_token, amount)
# if swap_result:
#     print("Успешно выполнен обмен:")
#     print("Входящий токен:", swap_result["fromToken"]["symbol"])
#     print("Исходящий токен:", swap_result["toToken"]["symbol"])
#     print("Количество входящего токена:", swap_result["fromToken"]["amount"])
#     print("Количество исходящего токена:", swap_result["toToken"]["amount"])
# else:
#     print("Не удалось выполнить обмен.")
