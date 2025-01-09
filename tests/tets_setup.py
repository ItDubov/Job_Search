import unittest
from unittest.mock import patch, MagicMock
import psycopg2
from scr.db_setup import initialize_db  # Импортируем функцию из вашего кода

class TestDBSetup(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_initialize_db_success(self, mock_connect):
        # Создаем моки для соединения и курсора
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Вызываем функцию для инициализации базы данных
        initialize_db()

        # Проверяем, что SQL-запросы на создание таблиц были выполнены
        mock_cursor.execute.assert_any_call("""
            CREATE TABLE companies (
               id SERIAL PRIMARY KEY,
               name VARCHAR(255) NOT NULL,
               industry VARCHAR(255),
               description TEXT,
               url VARCHAR(255)
            );
        """)
        mock_cursor.execute.assert_any_call("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                salary_min INT,
                salary_max INT,
                currency VARCHAR(3),
                description TEXT,
                url VARCHAR(255),
                company_id INT REFERENCES companies(id)
            );
        """)

        # Проверяем, что commit был вызван
        mock_connection.commit.assert_called_once()

    @patch('psycopg2.connect')
    def test_initialize_db_failure(self, mock_connect):
        # Мокаем ошибку при подключении
        mock_connect.side_effect = psycopg2.Error("Ошибка подключения")

        # Перехватываем вывод в консоль
        with self.assertRaises(psycopg2.Error):
            initialize_db()  # Функция должна выбросить исключение и вызвать ошибку подключения

if __name__ == '__main__':
    unittest.main()
