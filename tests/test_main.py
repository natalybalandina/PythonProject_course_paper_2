from pathlib import Path
from typing import Any, Dict, List

import pytest

from main import display_vacancies, user_interaction
from src.api_handler import HeadHunterAPI
from src.file_handler import JSONFileHandler
from src.helpers import parse_salary_range


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    """Фикстура для создания экземпляра HeadHunterAPI."""
    return HeadHunterAPI()


@pytest.fixture
def json_saver(tmp_path: Path) -> JSONFileHandler:
    """Фикстура для создания временного JSON-файла."""
    filename = tmp_path / "vacancies.json"
    saver = JSONFileHandler(filename=str(filename))
    return saver


def test_parse_salary_range() -> None:
    """
    Тестирует функцию parse_salary_range.
    Проверяет корректность парсинга диапазона зарплат.
    """
    # Корректный диапазон
    result = parse_salary_range("100000-200000")
    assert result == (100000.0, 200000.0)

    # Некорректный формат
    result = parse_salary_range("abc-def")
    assert result == (0, float("inf"))

    # Отсутствие разделителя
    result = parse_salary_range("150000")
    assert result == (0, float("inf"))

    # Диапазон с отрицательными числами
    result = parse_salary_range("-50000-150000")
    assert result == (0, float("inf"))


def test_display_vacancies(capsys: pytest.CaptureFixture) -> None:
    """
    Тестирует функцию display_vacancies.
    Проверяет корректность вывода списка вакансий через консоль.
    """
    test_vacancies: List[Dict[str, Any]] = [
        {
            "title": "Python Developer",
            "link": "http://example.com/python",
            "salary": 150000.0,
            "description": "Опыт работы с Python",
        },
        {
            "title": "Data Scientist",
            "link": "http://example.com/data",
            "salary": "Зарплата не указана",
            "description": "Машинное обучение",
        },
    ]

    display_vacancies(test_vacancies)
    captured = capsys.readouterr()

    expected_output = (
        "Название: Python Developer\n"
        "Ссылка: http://example.com/python\n"
        "Зарплата: 150000.0 руб.\n"
        "Описание: Опыт работы с Python\n"
        "----------------------------------------\n"
        "Название: Data Scientist\n"
        "Ссылка: http://example.com/data\n"
        "Зарплата: Зарплата не указана руб.\n"
        "Описание: Машинное обучение\n"
        "----------------------------------------\n"
    )

    assert captured.out.strip() == expected_output.strip()


def test_user_interaction(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    json_saver: JSONFileHandler,
) -> None:
    """
    Тестирует функцию user_interaction.
    Проверяет основные действия пользователя через консоль.
    """
    inputs = iter([
        "1",  # Выбор "Добавить вакансии из HeadHunter"
        "Python",  # Поисковый запрос
        "6",  # Выход из программы
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Имитация получения данных из API
    monkeypatch.setattr(
        HeadHunterAPI,
        "get_vacancies",
        lambda self, query: [
            {
                "title": "Test Vacancy",
                "link": "http://example.com/test",
                "salary": 120000.0,
                "description": "Тестовое описание",
            }
        ],
    )

    # Имитация сохранения данных в файл
    monkeypatch.setattr(JSONFileHandler, "add_vacancy", lambda self, vacancy_data: None)

    # Запуск функции user_interaction()
    user_interaction()

    # Проверка вывода
    captured = capsys.readouterr()
    assert "Вакансия «Test Vacancy» успешно добавлена." in captured.out
    assert "Выход из программы." in captured.out


def test_user_interaction_invalid_choice(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    json_saver: JSONFileHandler,
) -> None:
    """
    Тестирует обработку некорректного выбора в меню.
    """
    inputs = iter([
        "7",  # Некорректный выбор
        "6",  # Выход из программы
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Запуск функции user_interaction()
    user_interaction()

    # Проверка вывода
    captured = capsys.readouterr()
    assert "Некорректный выбор." in captured.out
    assert "Выход из программы." in captured.out


def test_user_interaction_empty_search_query(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    json_saver: JSONFileHandler,
) -> None:
    """
    Тестирует обработку пустого поискового запроса.
    """
    inputs = iter([
        "1",  # Выбор "Добавить вакансии из HeadHunter"
        "",  # Пустой поисковый запрос
        "6",  # Выход из программы
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Запуск функции user_interaction()
    user_interaction()

    # Проверка вывода
    captured = capsys.readouterr()
    assert "Поисковый запрос не может быть пустым." in captured.out
    assert "Выход из программы." in captured.out
