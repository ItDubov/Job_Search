import requests
from scr.config import HH_API_HEADERS

def test_hh_api():
    response = requests.get("https://api.hh.ru/employers", headers=HH_API_HEADERS, params={"text": "Яндекс"})
    if response.status_code == 200:
        print("Успешный запрос к HH API!")
        data = response.json()
        print(data["items"][0])  # Вывод первой компании
    else:
        print(f"Ошибка запроса: {response.status_code}")

if __name__ == "__main__":
    test_hh_api()
