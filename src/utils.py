from src.file_handler import JSONFileHandler


def sort_vacancies(vacancies: list, reverse: bool = True) -> list:
    """Сортировка вакансий по зарплате."""
    return sorted(vacancies, key=lambda v: v["salary"] or 0, reverse=reverse)


def save_vacancy_to_file(vacancy: dict, json_saver: JSONFileHandler) -> None:
    """
    Сохраняет вакансию в JSON-файл.
    :param vacancy: Словарь с данными о вакансии.
    :param json_saver: Экземпляр класса JSONFileHandler.
    """
    if not isinstance(vacancy, dict):  # Проверяем тип данных
        raise ValueError("Данные вакансии должны быть представлены как словарь.")
    json_saver.add_vacancy(vacancy)
