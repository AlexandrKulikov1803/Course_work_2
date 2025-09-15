import json
import os
from typing import Any

import pytest

from src.json_writer import JSONWriter
from src.vacancy import Vacancy

directory = os.getcwd()
default_path_file = os.path.join(directory, "data", "vacancies.json")


def test_json_writer_init() -> None:
    assert JSONWriter().path_json_file == default_path_file
    assert JSONWriter("").path_json_file == default_path_file
    assert JSONWriter("C:/vacancies.json").path_json_file == "C:/vacancies.json"


def test_get_data(file_data: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.json")
    with open(path_file, "w", encoding="utf-8") as file:
        json.dump(file_data, file, ensure_ascii=False)
    list_vacancies = JSONWriter(path_file).get_data()

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


def test_get_data_non_existent_file() -> None:
    path_file = os.path.join(directory, "data", "non-existent_file.json")
    assert JSONWriter(path_file).get_data() == []



def test_get_data_empty_file() -> None:
    path_file = os.path.join(directory, "data", "empty_file.json")

    with open(path_file, "a", encoding="UTF-8"):
        assert JSONWriter(path_file).get_data() == []



    os.remove(path_file)


def test_get_data_incorrect_content() -> None:
    path_file = os.path.join(directory, "data", "incorrect_content.json")

    with open(path_file, "a", encoding="UTF-8") as file:
        file.write("incorrect_content")

    assert JSONWriter(path_file).get_data() == []



    os.remove(path_file)


def test_add_data(vacancy_1: Vacancy, list_vacancies_1: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.json")
    json_saver = JSONWriter(path_file)

    assert len(json_saver.get_data()) == 2

    json_saver.add_data(vacancy_1)
    assert len(json_saver.get_data()) == 3

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies_1)
    json_saver.add_data(new_vacancies)
    assert len(json_saver.get_data()) == 5

    json_saver.add_data(new_vacancies)
    assert len(json_saver.get_data()) == 5

    vacancy = json_saver.get_data()
    assert vacancy[2] == vacancy_1
    assert vacancy[3] == new_vacancies[0]
    assert vacancy[4] == new_vacancies[1]


def test_del_data(vacancy_1: Vacancy, list_vacancies_1: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.json")
    json_saver = JSONWriter(path_file)

    assert len(json_saver.get_data()) == 5

    json_saver.del_data(vacancy_1)
    assert len(json_saver.get_data()) == 4

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies_1)
    json_saver.del_data(new_vacancies)
    assert len(json_saver.get_data()) == 2

    json_saver.del_data(new_vacancies)
    assert len(json_saver.get_data()) == 2

    json_saver.del_data()
    assert len(json_saver.get_data()) == 0
    with open(path_file, "r", encoding="UTF-8"):
        assert JSONWriter(path_file).get_data() == []

    os.remove(path_file)
