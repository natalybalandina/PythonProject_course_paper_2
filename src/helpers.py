import re
from typing import Optional


def clean_html(raw_html: Optional[str]) -> str:
    """
    Удаляет HTML-теги из строки.
    :param raw_html: Строка с HTML-тегами или None.
    :return: Чистая строка без HTML-тегов или "Описание отсутствует", если входная строка None.
    """
    if raw_html is None or not raw_html:
        return "Описание отсутствует"
    clean_text = re.sub(r"<.*?>", "", raw_html)  # Удаляем все теги между <>
    return clean_text.strip()


def parse_salary_range(salary_range_input: str) -> tuple:
    """
    Парсит диапазон зарплат из строки формата 'минимальная-максимальная'.
    :param salary_range_input: Строка с диапазоном зарплат.
    :return: Кортеж (min_salary, max_salary).
    """
    if not salary_range_input:  # Проверка на пустую строку
        return (0, float("inf"))  # Или другое значение по умолчанию
    try:
        min_salary, max_salary = map(float, salary_range_input.split("-"))
        if min_salary < 0 or max_salary < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        return min_salary, max_salary
    except ValueError:
        print("Некорректный формат диапазона зарплат. Используйте формат: минимум-максимум")
        return 0, float("inf")  # Если формат некорректный, используем весь диапазон
