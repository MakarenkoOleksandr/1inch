import requests

token_name = "example_token"
api_url = f"https://api.example.com/tokens?name={token_name}"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    # Обрабатывайте полученные данные по своему усмотрению
else:
    print("Ошибка при выполнении запроса")
