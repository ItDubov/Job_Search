import unittest
from unittest.mock import patch, MagicMock
from scr.db_manager import DBManager


class TestDBManager(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_save_company(self, mock_connect):
        # Мокаем соединение с базой данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Создаем тестовые данные компании
        company_data = {
            "name": "Test Company",
            "industries": [{"name": "IT"}],
            "description": "A leading tech company",
            "url": "https://example.com"
        }

        # Мокаем возврат результата от метода fetchone
        mock_cursor.fetchone.return_value = [1]  # Возвращаем ID 1

        # Тестируем сохранение компании
        db_manager = DBManager()
        with db_manager:
            company_id = db_manager.save_company(company_data)

        # Проверяем, что курсор был вызван с нужными параметрами
        mock_cursor.execute.assert_called_with(
            "INSERT INTO companies (name, industry, description, url) VALUES (%s, %s, %s, %s) RETURNING id",
            ("Test Company", "IT", "A leading tech company", "https://example.com")
        )
        mock_connection.commit.assert_called_once()

        # Проверяем, что возвращаемый company_id соответствует ID из фиктивного результата
        self.assertEqual(company_id, 1)

    @patch('psycopg2.connect')
    def test_get_companies_and_vacancies_count(self, mock_connect):
        # Мокаем соединение с базой данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Мокаем возврат данных
        mock_cursor.fetchall.return_value = [("Test Company", 5)]

        # Тестируем метод
        db_manager = DBManager()
        with db_manager:
            result = db_manager.get_companies_and_vacancies_count()

        # Проверяем правильность вызова запроса
        mock_cursor.execute.assert_called_with("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """)
        self.assertEqual(result, [("Test Company", 5)])

    @patch('psycopg2.connect')
    def test_get_avg_salary(self, mock_connect):
        # Мокаем соединение с базой данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Мокаем возврат данных для средней зарплаты
        mock_cursor.fetchone.return_value = [1500]

        # Тестируем метод
        db_manager = DBManager()
        with db_manager:
            result = db_manager.get_avg_salary()

        # Проверяем правильность вызова запроса
        mock_cursor.execute.assert_called_with("""
            SELECT AVG((salary_min + salary_max) / 2)
            FROM vacancies
            WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;
        """)
        self.assertEqual(result, 1500)

    @patch('psycopg2.connect')
    def test_get_vacancies_with_keyword(self, mock_connect):
        # Мокаем соединение с базой данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Мокаем возврат данных
        mock_cursor.fetchall.return_value = [("Developer", 1000, 2000, "https://example.com/vacancy/1")]

        # Тестируем метод
        db_manager = DBManager()
        with db_manager:
            result = db_manager.get_vacancies_with_keyword("Developer")

        # Проверяем правильность вызова запроса
        mock_cursor.execute.assert_called_with("""
            SELECT title, salary_min, salary_max, url
            FROM vacancies
            WHERE title ILIKE %s;
        """, ("%Developer%",))
        self.assertEqual(result, [("Developer", 1000, 2000, "https://example.com/vacancy/1")])


if __name__ == '__main__':
    unittest.main()
