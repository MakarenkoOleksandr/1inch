from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


chromedriver_path = 'D:/python/chromedriver.exe'

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Заходим на страницу
driver.get('https://app.1inch.io/')
wait = WebDriverWait(driver, 20)

# Выбираем монету
coin_list = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '.header-button')))
coin_list.click()

coins = driver.find_elements(By.CLASS_NAME, 'switch-network-item')

for coin in coins:
    if 'Arbitrum' in coin.text:
        driver.execute_script("arguments[0].click();", coin)
        break

# Подключаем кошелек
wallet_join = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '.header-button-light-blue')))
wallet_join.click()

terms = driver.find_element(By.CSS_SELECTOR, '.mat-checkbox-input')
driver.execute_script("arguments[0].click();", terms)

# platforms = driver.find_element(By.CSS_SELECTOR, '.app-network-item')

# for platform in platforms:
#     if 'Polygon' in platform.text:
#         platform.click()
#         break

wallets = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-id="Web3"]'))
)
wallets.click()

install_meta_mask = wait.until(
    EC.element_to_be_clickable(By.CSS_SELECTOR, '.dd-Va'))
install_meta_mask.click()

ActionChains(driver).send_keys(Keys.TAB).perform()
ActionChains(driver).send_keys(Keys.ENTER).perform()


time.sleep(5)
