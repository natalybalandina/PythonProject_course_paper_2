from pathlib import Path
from typing import Any, Dict

import pytest

from src.file_handler import JSONFileHandler
from src.utils import save_vacancy_to_file


@pytest.fixture
def json_saver(tmp_path: Path) -> JSONFileHandler:
    """Фикстура для создания временного JSON-файла."""
    filename = tmp_path / "vacancies.json"
    saver = JSONFileHandler(filename=str(filename))
    return saver


def test_save_vacancy_to_file(json_saver: JSONFileHandler) -> None:
    """Тестирует функцию save_vacancy_to_file."""
    # Создаем тестовую вакансию
    test_vacancy: Dict[str, Any] = {
        "title": "Python Developer",
        "link": "https://example.com/python-dev",
        "salary": 100000,
        "description": "Требуется опыт работы с Python."
    }

    # Сохраняем вакансию в файл
    save_vacancy_to_file(test_vacancy, json_saver)

    # Проверяем, что вакансия успешно добавлена
    data = json_saver._load_data()
    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"

    # Проверяем обработку некорректных данных
    with pytest.raises(ValueError, match="Вакансия должна содержать поле 'title'."):
        save_vacancy_to_file({"invalid": "data"}, json_saver)  # Передаем словарь без 'title'
