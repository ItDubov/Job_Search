import psycopg2
from scr.config import DB_CONFIG


def initialize_db():
    try:
        with psycopg2.connect(**DB_CONFIG, options="-c client_encoding=utf8") as conn:
            with conn.cursor() as cursor:
                # Пример создания таблиц
                cursor.execute("""
                    CREATE TABLE companies (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       industry VARCHAR(255),
                       description TEXT,
                       url VARCHAR(255)
                    );
                """)
                cursor.execute("""
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
                conn.commit()
                print("Таблицы успешно созданы!")
    except psycopg2.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
