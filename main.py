from scr.api_client import HHAPIClient
from scr.db_manager import DBManager
from scr.db_setup import initialize_db
import requests
import time

def main():
    initialize_db()

    companies = ["Яндекс", "Сбер", "Тинькофф", "Selecty", "Whales DMCC",
                 "IT-Solutions", "Rebotica", "Google", "idaproject"]

    for company in companies:
        try:
            employer_data = HHAPIClient.get_employers(company)
            print(f"Получены данные для компании: {company}")
        except requests.exceptions.ConnectionError as e:
            print(f"Ошибка подключения для {company}: {e}")
            time.sleep(5)

    with DBManager() as db:
        for company in companies:
            employer_data = HHAPIClient.get_employers(company)
            if not employer_data:
                print(f"Работодатель {company} не найден.")
                continue

            company_data = employer_data[0]
            print(f"Обработка компании: {company_data['name']}")

            # Сохраняем компанию в БД
            company_id = db.save_company(company_data)
            print(f"Сохранена компания с ID: {company_id}")

            # Получение вакансий для компании
            vacancies_response = HHAPIClient.get_vacancies(company_data['id'])
            if vacancies_response:
                db.save_vacancies(vacancies_response, company_id)
                print(f"Вакансии для компании {company_data['name']} сохранены.")
            else:
                print(f"Вакансии для компании {company_data['name']} не найдены.")

if __name__ == "__main__":
    main()
