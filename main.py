from typing import Any, Dict, List

from src.api_handler import HeadHunterAPI
from src.file_handler import JSONFileHandler
from src.helpers import clean_html, parse_salary_range
from src.vacancy import Vacancy


def display_vacancies(vacancies: List[Dict[str, Any]]) -> None:
    """
    Отображает список вакансий.
    :param vacancies: Список словарей с данными о вакансиях.
    """
    for vacancy in vacancies:
        title = vacancy.get("title", "Без названия")
        link = vacancy.get("link", "Ссылка отсутствует")
        salary = vacancy.get("salary", "Зарплата не указана")
        description = clean_html(vacancy.get("description", "Описание отсутствует") or "Описание отсутствует")

        print(f"Название: {title}")
        print(f"Ссылка: {link}")
        print(f"Зарплата: {salary} руб.")
        print(f"Описание: {description}")
        print("-" * 40)


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем через консоль."""
    json_saver = JSONFileHandler()

    while True:
        print("\nМеню:")
        print("1. Добавить вакансии из HeadHunter")
        print("2. Удалить вакансию по ID")
        print("3. Фильтровать вакансии по ключевым словам")
        print("4. Фильтровать вакансии по зарплате")
        print("5. Показать все вакансии")
        print("6. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            search_query = input("Введите поисковый запрос: ").strip()
            if not search_query:
                print("Поисковый запрос не может быть пустым.")
                continue
            hh_api = HeadHunterAPI()
            try:
                hh_vacancies = hh_api.get_vacancies(search_query)
                for vacancy in hh_vacancies:
                    try:
                        vacancy_data = Vacancy(
                            title=vacancy["title"],
                            link=vacancy["link"],
                            salary=vacancy.get("salary", "Зарплата не указана"),
                            description=vacancy.get("description", "Описание отсутствует"),
                        ).to_dict()
                        json_saver.add_vacancy(vacancy_data)
                        print(f"Вакансия «{vacancy['title']}» успешно добавлена.")  # Явное сообщение
                    except ValueError as e:
                        print(f"Ошибка при добавлении вакансии: {e}")
            except ConnectionError as e:
                print(f"Ошибка подключения к API: {e}")

        elif choice == "2":
            vacancy_id = input("Введите ID вакансии для удаления: ").strip()
            if vacancy_id.isdigit():
                json_saver.delete_vacancy(int(vacancy_id))
                print(f"Вакансия с ID {vacancy_id} удалена.")  # Явное сообщение
            else:
                print("Некорректный ID.")

        elif choice == "3":
            filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
            filtered_vacancies = json_saver.filter_vacancies(filter_words)
            display_vacancies(filtered_vacancies)

        elif choice == "4":
            salary_range_input = input("Введите диапазон зарплат (минимум-максимум): ").strip()
            salary_range = parse_salary_range(salary_range_input)
            if salary_range == (0, float("inf")):
                print("Некорректный формат диапазона зарплат.")
            else:
                filtered_vacancies = json_saver.filter_vacancies_by_salary(salary_range)
                display_vacancies(filtered_vacancies)

        elif choice == "5":
            all_vacancies = json_saver.filter_vacancies([])
            display_vacancies(all_vacancies)

        elif choice == "6":
            print("Выход из программы.")  # Явное сообщение
            break

        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    user_interaction()
