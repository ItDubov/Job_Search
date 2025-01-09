import psycopg2
from scr.config import DB_CONFIG
try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("Подключение к базе данных успешно!")
    conn.close()
except psycopg2.Error as e:
    print(f"Ошибка подключения: {e}")
