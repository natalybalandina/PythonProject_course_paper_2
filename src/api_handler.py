from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union, cast

import requests

from src.helpers import clean_html


class APIHandler(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями."""

    @abstractmethod
    def connect(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Метод для подключения к API.
        :param url: URL-адрес для подключения.
        :param params: Параметры запроса в виде словаря.
        :return: Словарь с данными ответа API.
        :raises ConnectionError: Если произошла ошибка подключения к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Метод для получения вакансий по ключевому слову.
        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей, где каждый словарь представляет вакансию.
        """
        pass


class HeadHunterAPI(APIHandler):
    """
    Класс для работы с API HeadHunter.
    Реализует методы для подключения к API и получения вакансий.
    """

    _BASE_URL = "https://api.hh.ru/vacancies"

    def connect(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подключение к API HeadHunter.

        :param url: URL-адрес для подключения (обычно _BASE_URL).
        :param params: Параметры запроса, например, 'text' для ключевого слова.
        :return: Словарь с данными ответа API HeadHunter.
        :raises ConnectionError: Если запрос вернул статус, отличный от 200.
        """
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API HeadHunter: {response.status_code} - {response.text}")

        # Явно указываем, что ответ является словарем, используя cast для типа
        return cast(Dict[str, Any], response.json())

    def _get_formatted_salary(self, item_salary: Dict[str, Any] | None) -> Union[int, str]:
        """
        Форматирует информацию о зарплате из данных вакансии.
        Возвращает значение "from" если оно есть и не равно None,
        иначе "Зарплата не указана".
        """
        if item_salary and item_salary.get("from") is not None:
            return item_salary["from"]

        return "Зарплата не указана"

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий с hh.ru по ключевому слову.
        :param keyword: Ключевое слово для поиска вакансий.
        :return: Список словарей, где каждый словарь представляет вакансию
                 с полями 'title', 'link', 'salary', 'description'.
        """
        # Получение вакансий только с указанной зарплатой
        params = {"text": keyword, "per_page": 100, "only_with_salary": True}
        try:
            data = self.connect(self._BASE_URL, params)
            vacancies_list = []
            for item in data.get("items", []):
                vacancy = {
                    "title": item.get("name", "Название не указано"),
                    "link": item.get("alternate_url", "Ссылка не указана"),
                    "salary": self._get_formatted_salary(item.get("salary")),
                    "description": clean_html(item.get("snippet", {}).get("requirement", "Описание отсутствует")),
                }
                vacancies_list.append(vacancy)
            return vacancies_list

        except ConnectionError as e:
            print(f"Произошла ошибка при получении вакансий HeadHunter: {e}")
            return []
        except Exception as e:
            # Общий перехват исключений для обработки непредвиденных ошибок при обработке данных
            print(f"Произошла непредвиденная ошибка при обработке вакансий HeadHunter: {e}")
            return []
