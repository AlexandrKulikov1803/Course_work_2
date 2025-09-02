import json
import os
from typing import Any

import pytest

from src.text_writer import TXTWriter
from src.vacancy import Vacancy
from tests.conftest import list_vacancies

directory = os.getcwd()
default_path_file = os.path.join(directory, "data", "vacancies.txt")


def test_json_writer_init() -> None:
    assert TXTWriter().path_json_file == default_path_file
    assert TXTWriter("C:/vacancies.txt").path_json_file == "C:/vacancies.txt"


def test_get_data(file_data: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.txt")
    with open(path_file, "w", encoding="utf-8") as file:
        json.dump(file_data, file, ensure_ascii=False)
    list_vacancies = TXTWriter(path_file).get_data()

    assert list_vacancies[0].name == "Аналитик данных (Data Analyst)"
    assert list_vacancies[0].url == "https://api.hh.ru/vacancies/124265987?host=hh.ru"
    assert list_vacancies[0].salary == "Не указана"
    assert list_vacancies[0].experience == "От 1 года до 3 лет"

    assert list_vacancies[1].name == "Инженер по ручному тестированию"
    assert list_vacancies[1].url == "https://api.hh.ru/vacancies/124477766?host=hh.ru"
    assert list_vacancies[1].salary == "Не указана"
    assert list_vacancies[1].experience == "От 2 до 6 лет"

    with pytest.raises(IndexError):
        print(list_vacancies[2])


def test_get_data_non_existent_file(capsys: Any) -> None:
    path_file = os.path.join(directory, "data", "non-existent_file.txt")
    assert TXTWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл не найден"


def test_get_data_empty_file(capsys: Any) -> None:
    path_file = os.path.join(directory, "data", "empty_file.txt")

    with open(path_file, "a", encoding="UTF-8"):
        assert TXTWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл пустой"

    os.remove(path_file)


def test_get_data_incorrect_content(capsys: Any) -> None:
    path_file = os.path.join(directory, "data", "incorrect_content.txt")

    with open(path_file, "a", encoding="UTF-8") as file:
        file.write("incorrect_content")

    assert TXTWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл содержит некорректные данные"

    os.remove(path_file)


def test_add_data(vacancy_1: Vacancy, list_vacancies: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.txt")
    json_saver = TXTWriter(path_file)

    assert len(json_saver.get_data()) == 2

    json_saver.add_data(vacancy_1)
    assert len(json_saver.get_data()) == 3

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies)
    json_saver.add_data(new_vacancies)
    assert len(json_saver.get_data()) == 5

    json_saver.add_data(new_vacancies)
    assert len(json_saver.get_data()) == 5

    vacancy = json_saver.get_data()
    assert vacancy[2] == vacancy_1
    assert vacancy[3] == new_vacancies[0]
    assert vacancy[4] == new_vacancies[1]


def test_del_data(vacancy_1: Vacancy, list_vacancies: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.txt")
    json_saver = TXTWriter(path_file)

    assert len(json_saver.get_data()) == 5

    json_saver.del_data(vacancy_1)
    assert len(json_saver.get_data()) == 4

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies)
    json_saver.del_data(new_vacancies)
    assert len(json_saver.get_data()) == 2

    json_saver.del_data(new_vacancies)
    assert len(json_saver.get_data()) == 2

    json_saver.del_data()
    assert len(json_saver.get_data()) == 0
    with open(path_file, "r", encoding="UTF-8"):
        assert TXTWriter(path_file).get_data() == []

    os.remove(path_file)
