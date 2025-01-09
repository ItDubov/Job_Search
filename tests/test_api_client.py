import unittest
from unittest.mock import patch
from scr.api_client import HHAPIClient


class TestHHAPIClient(unittest.TestCase):

    @patch('requests.get')
    def test_get_employers_success(self, mock_get):
        # Мокаем успешный ответ от API
        mock_response = {
            "items": [
                {"name": "Яндекс", "id": 1},
                {"name": "Сбер", "id": 2},
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        query = "IT"
        result = HHAPIClient.get_employers(query)

        # Проверяем, что запрос возвращает правильные данные
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Яндекс")
        self.assertEqual(result[1]["name"], "Сбер")

    @patch('requests.get')
    def test_get_employers_failure(self, mock_get):
        # Мокаем ошибку при запросе
        mock_get.return_value.status_code = 500  # Серверная ошибка
        mock_get.return_value.json.return_value = {}

        query = "IT"
        result = HHAPIClient.get_employers(query)

        # Проверяем, что при ошибке вернется пустой список
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        # Мокаем успешный ответ для вакансий
        mock_response = {
            "items": [
                {"name": "Python Developer", "id": 1, "salary": {"from": 1000, "to": 2000}},
                {"name": "Java Developer", "id": 2, "salary": {"from": 1500, "to": 2500}},
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        employer_id = 1
        result = HHAPIClient.get_vacancies(employer_id)

        # Проверяем, что запрос возвращает правильные данные
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Python Developer")
        self.assertEqual(result[1]["name"], "Java Developer")
