import json
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

import pytest

from src.file_handler import JSONFileHandler


@pytest.fixture
def json_file_handler() -> JSONFileHandler:
    return JSONFileHandler("test_vacancies.json")


def test_add_vacancy(json_file_handler: JSONFileHandler) -> None:
    vacancy_data: Dict[str, Any] = {
        "id": 1,
        "title": "Python Developer",
        "link": "https://example.com",
        "salary": 100000,
        "description": "<b>Описание</b> вакансии",
    }

    mock_data = json.dumps([])  # Изначально файл пуст
    with patch("builtins.open", mock_open(read_data=mock_data)), patch(
        "src.file_handler.JSONFileHandler._save_data"
    ) as mock_save:
        json_file_handler.add_vacancy(vacancy_data)
        mock_save.assert_called_once()
        # Проверка, что данные были очищены
        assert vacancy_data["description"] == "Описание вакансии"


def test_delete_vacancy(json_file_handler: JSONFileHandler) -> None:
    vacancy_data: Dict[str, Any] = {
        "id": 1,
        "title": "Python Developer",
        "link": "https://example.com",
        "salary": 100000,
        "description": "Описание вакансии",
    }

    mock_data = json.dumps([vacancy_data])  # В файле есть одна вакансия
    with patch("builtins.open", mock_open(read_data=mock_data)), patch(
        "src.file_handler.JSONFileHandler._save_data"
    ) as mock_save:
        json_file_handler.delete_vacancy(1)
        mock_save.assert_called_once()  # Убедитесь, что _save_data был вызван

        # Проверка, что _save_data был вызван с пустым списком
        mock_save.assert_called_once_with([])  # Ожидаем, что после удаления списка вакансий будет пустым


def test_filter_vacancies(json_file_handler: JSONFileHandler) -> None:
    mock_data = json.dumps(
        [
            {"id": 1, "title": "Python Developer", "description": "Описание Python"},
            {"id": 2, "title": "Java Developer", "description": "Описание Java"},
        ]
    )

    with patch("builtins.open", mock_open(read_data=mock_data)):
        filtered_vacancies: List[Dict[str, Any]] = json_file_handler.filter_vacancies(["Python"])
        assert len(filtered_vacancies) == 1
        assert filtered_vacancies[0]["title"] == "Python Developer"


def test_filter_vacancies_by_salary(json_file_handler: JSONFileHandler) -> None:
    mock_data = json.dumps(
        [
            {"id": 1, "title": "Python Developer", "salary": 100000},
            {"id": 2, "title": "Java Developer", "salary": 80000},
            {"id": 3, "title": "C++ Developer", "salary": 120000},
        ]
    )

    with patch("builtins.open", mock_open(read_data=mock_data)):
        filtered_vacancies: List[Dict[str, Any]] = json_file_handler.filter_vacancies_by_salary((90000, 130000))
        assert len(filtered_vacancies) == 2
        assert all(v["salary"] >= 90000 and v["salary"] <= 130000 for v in filtered_vacancies)


def test_load_data_empty_file(json_file_handler: JSONFileHandler) -> None:
    with patch("builtins.open", mock_open(read_data="")):
        data: List[Dict[str, Any]] = json_file_handler._load_data()
        assert data == []


@pytest.fixture
def json_saver(tmp_path: Path) -> JSONFileHandler:
    """Фикстура для создания временного JSON-файла."""
    filename = tmp_path / "vacancies.json"
    saver = JSONFileHandler(filename=str(filename))
    return saver


def test_filter_vacancies_with_none_description(json_saver: JSONFileHandler) -> None:
    """Тестирует фильтрацию вакансий с отсутствующим описанием."""
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
            "salary": 200000.0,
            "description": None,
        },
        {
            "title": "Junior Developer",
            "link": "http://example.com/junior",
            "salary": "Зарплата не указана",
            "description": "Без опыта работы",
        },
    ]

    for vacancy in test_vacancies:  # vacancy здесь будет Dict[str, Any]
        json_saver.add_vacancy(vacancy)

    filtered = json_saver.filter_vacancies(["Python"])
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Python Developer"


def test_filter_vacancies_by_salary_with_none_salary(json_saver: JSONFileHandler) -> None:
    """Тестирует фильтрацию вакансий по зарплате с отсутствующей зарплатой."""
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
            "salary": None,
            "description": "Знание машинного обучения",
        },
        {
            "title": "Junior Developer",
            "link": "http://example.com/junior",
            "salary": "Зарплата не указана",
            "description": "Без опыта работы",
        },
    ]

    for vacancy in test_vacancies:  # vacancy здесь будет Dict[str, Any]
        json_saver.add_vacancy(vacancy)

    filtered = json_saver.filter_vacancies_by_salary((100000.0, 200000.0))
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Python Developer"
