import requests
from scr.config import HH_API_HEADERS


class HHAPIClient:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employers(query):
        response = requests.get(
            f"{HHAPIClient.BASE_URL}/employers",
            headers=HH_API_HEADERS,
            params={"text": query}
        )
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print(f"Ошибка при запросе работодателей: {response.status_code}")
            return []

    @staticmethod
    def get_vacancies(employer_id):
        response = requests.get(
            f"{HHAPIClient.BASE_URL}/vacancies",
            headers=HH_API_HEADERS,
            params={"employer_id": employer_id}
        )
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print(f"Ошибка при запросе вакансий: {response.status_code}")
            return []
