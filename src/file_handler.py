import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple

from src.helpers import clean_html


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Добавляет вакансию в файл."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: int) -> None:
        """Удаляет вакансию из файла по ID."""
        pass

    @abstractmethod
    def filter_vacancies(self, filter_words: List[str]) -> List[Dict[str, Any]]:
        """Фильтрует вакансии по ключевым словам."""
        pass

    @abstractmethod
    def filter_vacancies_by_salary(self, salary_range: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Фильтрует вакансии по диапазону зарплат."""
        pass


class JSONFileHandler(FileHandler):
    """Класс для работы с JSON-файлами."""

    def __init__(self, filename: str = "data/test_vacancies.json") -> None:
    # Строка для проверки работоспособности кода. Записывает информацию в test_vacancies.json
    # def __init__(self, filename: str = "data/vacancies.json") -> None:
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создает файл, если он не существует."""
        Path(self._filename).parent.mkdir(parents=True, exist_ok=True)
        if not Path(self._filename).exists():
            with open(self._filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _load_data(self) -> List[Dict[str, Any]]:
        """Загружает данные из JSON-файла."""
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Убедимся, что данные - это список словарей
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    return data
                else:
                    return []  # Возвращаем пустой список, если данные некорректны
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[Dict[str, Any]]) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Добавляет вакансию в JSON-файл."""

        # Проверка на наличие необходимых полей
        required_fields = ["title", "link", "salary", "description"]
        for field in required_fields:
            if field not in vacancy_data:
                raise ValueError(f"Вакансия должна содержать поле '{field}'.")

        # Если поле 'description' отсутствует, можно установить значение по умолчанию
        vacancy_data["description"] = vacancy_data.get("description", "Описание отсутствует")

        # Обработка HTML
        vacancy_data["description"] = clean_html(vacancy_data["description"])

        data = self._load_data()
        if vacancy_data not in data:  # Проверка на дубликаты
            data.append(vacancy_data)
            self._save_data(data)
            print(f"Вакансия '{vacancy_data['title']}' успешно добавлена.")

    def delete_vacancy(self, vacancy_id: int) -> None:
        """Удаляет вакансию из JSON-файла по ID."""
        data = self._load_data()
        data = [v for v in data if v.get("id") != vacancy_id]
        self._save_data(data)
        print(f"Вакансия с ID {vacancy_id} удалена.")

    def filter_vacancies(self, filter_words: List[str]) -> List[Dict]:
        """
        Фильтрует вакансии по ключевому слову в описании.
        :param filter_word: Ключевое слово для фильтрации.
        :return: Список словарей с отфильтрованными вакансиями.
        """
        data = self._load_data()
        if not data or not isinstance(data, list):
            return []

        # Если фильтр пуст, возвращаем все вакансии
        if not filter_words:
            return data

        return [
            v
            for v in data
            if isinstance(v, dict)
            and any(
                word.lower()
                in (clean_html(v.get("description", "Описание отсутствует") or "Описание отсутствует")).lower()
                for word in filter_words
            )
        ]

    def filter_vacancies_by_salary(self, salary_range: Tuple[float, float]) -> List[Dict[str, Any]]:
        """
        Фильтрует вакансии по диапазону зарплат.
        :param salary_range: Кортеж (min_salary, max_salary).
        :return: Список отфильтрованных вакансий.
        """
        data = self._load_data()
        min_salary, max_salary = salary_range

        return [
            v
            for v in data
            if isinstance(v, dict)
            and isinstance(v.get("salary"), (float, int))
            and min_salary <= v["salary"] <= max_salary
        ]
