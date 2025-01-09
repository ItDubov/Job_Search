import psycopg2
from scr.config import DB_CONFIG


class DBManager:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        # Устанавливаем соединение с базой данных
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Закрываем соединение и курсор
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def save_vacancies(self, vacancies, company_id):
        for vacancy in vacancies:
            salary_min = vacancy["salary"]["from"] if vacancy["salary"] else None
            salary_max = vacancy["salary"]["to"] if vacancy["salary"] else None
            currency = vacancy["salary"]["currency"] if vacancy["salary"] else None
            self.cursor.execute(
                """
                INSERT INTO vacancies (title, salary_min, salary_max, currency, description, url, company_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy["name"], salary_min, salary_max, currency,
                 vacancy["snippet"]["responsibility"], vacancy["alternate_url"], company_id)
            )
        self.connection.commit()

    def save_company(self, company_data):
        """Пример метода для сохранения компании в БД."""
        self.cursor.execute(
            "INSERT INTO companies (name, industry, description, url) VALUES (%s, %s, %s, %s) RETURNING id",
            (
                company_data["name"],
                company_data.get("industries", [{}])[0].get("name"),
                company_data.get("description", ""),
                company_data.get("url", "")
            )
        )
        company_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return company_id

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.salary_min, vacancies.salary_max, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("""
            SELECT AVG((salary_min + salary_max) / 2)
            FROM vacancies
            WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL;
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT title, salary_min, salary_max, url
            FROM vacancies
            WHERE (salary_min + salary_max) / 2 > %s;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT title, salary_min, salary_max, url
            FROM vacancies
            WHERE title ILIKE %s;
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
