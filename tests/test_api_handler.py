import pytest

from src.api_handler import HeadHunterAPI


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    return HeadHunterAPI()


def test_get_vacancies(hh_api: HeadHunterAPI) -> None:
    """Тестирует метод get_vacancies()."""
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    # Проверяем, что результат — это список
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0  # Убедимся, что есть хотя бы одна вакансия

    # Проверяем структуру каждой вакансии
    for vacancy in vacancies:
        assert "title" in vacancy  # Вместо 'name' используем 'title'
        assert "link" in vacancy
        assert "salary" in vacancy
        assert "description" in vacancy


def test_get_vacancies_with_salary(hh_api: HeadHunterAPI) -> None:
    """Тестирует получение вакансий с корректной зарплатой."""
    vacancies = hh_api.get_vacancies("Python")
    assert isinstance(vacancies, list)
    for vacancy in vacancies:
        assert "title" in vacancy
        assert "link" in vacancy
        assert "salary" in vacancy
        assert "description" in vacancy
        if isinstance(vacancy["salary"], str):
            assert vacancy["salary"] == "Зарплата не указана"


def test_get_vacancies_without_salary(hh_api: HeadHunterAPI) -> None:
    """Тестирует получение вакансий без зарплаты."""
    vacancies = hh_api.get_vacancies("Junior Developer")
    for vacancy in vacancies:
        if vacancy["salary"] == "Зарплата не указана":
            assert isinstance(vacancy["salary"], str)
