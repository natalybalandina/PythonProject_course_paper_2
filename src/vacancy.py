from typing import Optional, Union

from src.helpers import clean_html


class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ["_title", "_link", "_salary", "_description"]

    def __init__(self, title: str, link: str, salary: Optional[Union[float, str]], description: str) -> None:
        self._title = self._validate_title(title)
        self._link = self._validate_link(link)

        # Присваиваем _salary, который может быть как float, так и str
        if salary is None:
            self._salary: Union[float, str] = "Зарплата не указана"  # строка, если salary None
        else:
            self._salary = self._validate_salary(salary)  # Присваиваем значение, которое может быть float или str

        self._description = self._validate_description(description)

    @staticmethod
    def _validate_title(title: str) -> str:
        if not title:
            raise ValueError("Название вакансии не может быть пустым.")
        return title

    @staticmethod
    def _validate_link(link: str) -> str:
        if not link.startswith("http"):
            raise ValueError("Некорректная ссылка.")
        return link

    @staticmethod
    def _validate_salary(salary: Optional[Union[float, str]]) -> Union[float, str]:
        if salary is None or (isinstance(salary, str) and salary.lower() == "зарплата не указана"):
            return "Зарплата не указана"
        if isinstance(salary, (int, float)):
            return float(salary)  # Приводим к float
        try:
            return float(salary.split("-")[0].replace(" ", "").replace("руб.", ""))
        except (ValueError, AttributeError):
            return "Зарплата не указана"

    @staticmethod
    def _validate_description(description: Optional[str]) -> str:
        cleaned_description = clean_html(description or "")
        return cleaned_description if cleaned_description else "Описание отсутствует"

    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "link": self._link,
            "salary": self._salary,
            "description": self._description,
        }

    @property
    def title(self) -> str:
        return self._title

    @property
    def salary(self) -> Union[float, str]:
        return self._salary

    def __str__(self) -> str:
        return f"{self._title}, {self._salary} руб.\n{self._description}\nСсылка: {self._link}"

    def __lt__(self, other: "Vacancy") -> bool:
        if isinstance(self._salary, str) or isinstance(other.salary, str):
            return False  # Если хотя бы одно из значений зарплаты - строка, сравнивать нельзя
        return float(self._salary) < float(other.salary)  # Приведем оба к float для корректного сравнения

    def __gt__(self, other: "Vacancy") -> bool:
        if isinstance(self._salary, str) or isinstance(other.salary, str):
            return False  # Если хотя бы одно из значений зарплаты - строка, сравнивать нельзя
        return float(self._salary) > float(other.salary)  # Приведем оба к float для корректного сравнения
