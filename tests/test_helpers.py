from src.helpers import clean_html, parse_salary_range


def test_clean_html() -> None:
    """Тестирует функцию clean_html."""
    # Примеры с HTML-тегами
    assert clean_html("<highlighttext>Python</highlighttext>") == "Python"
    assert clean_html("<b>Senior</b> <i>QA</i> Engineer") == "Senior QA Engineer"
    assert clean_html("Опыт работы с <highlighttext>Python</highlighttext> и SQL") == "Опыт работы с Python и SQL"

    # Примеры без HTML-тегов
    assert clean_html("Программист Python") == "Программист Python"

    # Проверка пустой строки
    assert clean_html("") == "Описание отсутствует"  # Ожидаемое поведение для пустой строки


def test_parse_salary_range() -> None:
    """Тестирует функцию parse_salary_range."""
    # Корректный диапазон
    result = parse_salary_range("100000-200000")
    assert result == (100000.0, 200000.0)

    # Некорректный формат
    result = parse_salary_range("abc-def")
    assert result == (0, float("inf"))

    # Отсутствие разделителя
    result = parse_salary_range("100000")
    assert result == (0, float("inf"))

    # Диапазон с отрицательными числами
    result = parse_salary_range("-50000-150000")
    assert result == (
        0,
        float("inf"),
    )  # Функция должна игнорировать отрицательные числа <button class="citation-flag" data-index="1">
