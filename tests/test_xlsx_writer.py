import os
import warnings

import pandas as pd
import pytest

from src.vacancy import Vacancy
from src.xlsx_writer import XLSXWriter

directory = os.getcwd()
default_path_file = os.path.join(directory, "data", "vacancies.xlsx")


def test_xlsx_writer_init() -> None:
    assert XLSXWriter().path_xlsx_file == default_path_file
    assert XLSXWriter("").path_xlsx_file == default_path_file
    assert XLSXWriter("C:/vacancies.xlsx").path_xlsx_file == "C:/vacancies.xlsx"


def test_get_data(file_data: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.xlsx")
    data = pd.DataFrame(file_data)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        data.to_excel(path_file, index=False)
        list_vacancies = XLSXWriter(path_file).get_data()

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
    path_file = os.path.join(directory, "data", "non-existent_file.xlsx")
    assert XLSXWriter(path_file).get_data() == []


def test_get_data_empty_file() -> None:
    path_file = os.path.join(directory, "data", "empty_file.xlsx")
    df = pd.DataFrame()
    df.to_excel(path_file, index=False)
    assert XLSXWriter(path_file).get_data() == []

    os.remove(path_file)


def test_get_data_incorrect_content() -> None:
    path_file = os.path.join(directory, "data", "incorrect_content.xlsx")
    df = pd.DataFrame(
        {
            "name": ["Python Developer"],
            "url": ["https://..."],
            "salary": [50000],
            "experience": ["Нет опыта"],
            "address": ["Moscow"],
        }
    )
    df.to_excel(path_file, index=False)
    assert XLSXWriter(path_file).get_data() == []

    os.remove(path_file)


def test_add_data(vacancy_1: Vacancy, list_vacancies_1: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.xlsx")
    xlsx_saver = XLSXWriter(path_file)

    assert len(xlsx_saver.get_data()) == 2

    xlsx_saver.add_data(vacancy_1)
    assert len(xlsx_saver.get_data()) == 3

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies_1)
    xlsx_saver.add_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 5

    xlsx_saver.add_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 5

    vacancy = xlsx_saver.get_data()
    assert vacancy[2] == vacancy_1
    assert vacancy[3] == new_vacancies[0]
    assert vacancy[4] == new_vacancies[1]


def test_del_data(vacancy_1: Vacancy, list_vacancies_1: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.xlsx")
    xlsx_saver = XLSXWriter(path_file)

    assert len(xlsx_saver.get_data()) == 5

    xlsx_saver.del_data(vacancy_1)
    assert len(xlsx_saver.get_data()) == 4

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies_1)
    xlsx_saver.del_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 2

    xlsx_saver.del_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 2

    xlsx_saver.del_data()
    assert len(xlsx_saver.get_data()) == 0
    assert XLSXWriter(path_file).get_data() == []

    os.remove(path_file)
