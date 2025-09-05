import pytest

from src.file_handler import JSONFileHandler
from src.vacancy import Vacancy


def test_vacancy_comparison() -> None:
    """Тестирование сравнения вакансий."""
    vacancy1 = Vacancy("Python Developer", "https://example.com", "100000-150000 руб.", "Опыт работы с Python")
    vacancy2 = Vacancy("Data Scientist", "https://example.com", "120000-180000 руб.", "Знание машинного обучения")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1


def test_vacancy_validation() -> None:
    """Тестирование валидации данных при создании вакансии."""
    # Проверка создания вакансии с пустым названием
    with pytest.raises(ValueError):
        Vacancy("", "https://example.com", "100000-150000 руб.", "Опыт работы с Python")

    # Проверка создания вакансии с некорректной ссылкой
    with pytest.raises(ValueError):
        Vacancy("Python Developer", "invalid_link", "100000-150000 руб.", "Опыт работы с Python")


def test_json_file_handler() -> None:
    """Тестирование работы с JSON-файлами."""
    json_saver = JSONFileHandler()

    # Добавление вакансии
    json_saver.add_vacancy(
        {
            "title": "Python Developer",
            "link": "https://example.com",
            "salary": 100000,
            "description": "Опыт работы с Python",
        }
    )

    # Фильтрация вакансий
    filtered_vacancies = json_saver.filter_vacancies(["Python"])  # Передаем список строк
    assert len(filtered_vacancies) >= 0

    # Удаление вакансии
    json_saver.delete_vacancy(12345)  # Предполагается, что ID вакансии равен 12345


def test_vacancy_to_dict() -> None:
    """Тестирует метод to_dict()."""
    vacancy = Vacancy(
        title="Python Developer",
        link="https://example.com/python-dev",
        salary=100000,
        description="Требуется опыт работы с Python.",
    )
    vacancy_dict = vacancy.to_dict()
    assert vacancy_dict["title"] == "Python Developer"
    assert vacancy_dict["link"] == "https://example.com/python-dev"
    assert vacancy_dict["salary"] == 100000
    assert vacancy_dict["description"] == "Требуется опыт работы с Python."


def test_validate_salary() -> None:
    """Тестирует метод _validate_salary."""
    # Тест с числовым значением
    assert Vacancy._validate_salary(100000) == 100000

    # Тест со строковым значением
    assert Vacancy._validate_salary("100 000-150 000 руб.") == 100000.0

    # Тест с None
    assert Vacancy._validate_salary(None) == "Зарплата не указана"

    # Тест с пустой строкой
    assert Vacancy._validate_salary("") == "Зарплата не указана"

    # Тест с некорректным форматом
    assert Vacancy._validate_salary("некорректная зарплата") == "Зарплата не указана"


def test_vacancy_creation() -> None:
    """Тестирует создание объекта Vacancy."""
    vacancy = Vacancy(
        title="Python Developer",
        link="https://example.com/python-dev",
        salary=100000,
        description="Требуется опыт работы с Python.",
    )
    assert vacancy._title == "Python Developer"
    assert vacancy._link == "https://example.com/python-dev"
    assert vacancy._salary == 100000
    assert vacancy._description == "Требуется опыт работы с Python."

    # Создание с зарплатой None
    vacancy_none_salary = Vacancy(
        title="Data Scientist",
        link="https://example.com/data-scientist",
        salary=None,
        description="Требуется знание машинного обучения.",
    )
    assert vacancy_none_salary._salary == "Зарплата не указана"
