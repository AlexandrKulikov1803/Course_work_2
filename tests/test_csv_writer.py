import os
from typing import Any

import pandas as pd
import pytest

from src.csv_writer import CSVWriter
from src.vacancy import Vacancy

directory = os.getcwd()
default_path_file = os.path.join(directory, "data", "vacancies.csv")


def test_csv_writer_init() -> None:
    assert CSVWriter().path_csv_file == default_path_file
    assert CSVWriter("C:/vacancies.csv").path_csv_file == "C:/vacancies.csv"


def test_get_data(file_data: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.csv")
    data = pd.DataFrame(file_data)
    data.to_csv(path_file, index=False, encoding="utf-8-sig", sep=";")
    list_vacancies = CSVWriter(path_file).get_data()

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
    path_file = os.path.join(directory, "data", "non-existent_file.csv")
    assert CSVWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл не найден"


def test_get_data_empty_file(capsys: Any) -> None:
    path_file = os.path.join(directory, "data", "empty_file.csv")
    df = pd.DataFrame()
    df.to_csv(path_file, index=False, encoding="utf-8", sep=";")
    assert CSVWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл пустой"

    df = pd.DataFrame({"name": [], "url": [], "salary": [], "experience": []})

    df.to_csv(path_file, index=False, encoding="utf-8", sep=";")
    assert CSVWriter(path_file).get_data() == []

    message = capsys.readouterr()
    assert message.out.strip() == "Файл пустой"

    os.remove(path_file)


def test_add_data(vacancy_1: Vacancy, list_vacancies: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.csv")
    xlsx_saver = CSVWriter(path_file)

    assert len(xlsx_saver.get_data()) == 2

    xlsx_saver.add_data(vacancy_1)
    assert len(xlsx_saver.get_data()) == 3

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies)
    xlsx_saver.add_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 5

    xlsx_saver.add_data(new_vacancies)
    assert len(xlsx_saver.get_data()) == 5

    vacancy = xlsx_saver.get_data()
    assert vacancy[2] == vacancy_1
    assert vacancy[3] == new_vacancies[0]
    assert vacancy[4] == new_vacancies[1]


def test_del_data(vacancy_1: Vacancy, list_vacancies: list) -> None:
    path_file = os.path.join(directory, "data", "correct_content.csv")
    csv_saver = CSVWriter(path_file)

    assert len(csv_saver.get_data()) == 5

    csv_saver.del_data(vacancy_1)
    assert len(csv_saver.get_data()) == 4

    new_vacancies = Vacancy.cast_to_object_list(list_vacancies)
    csv_saver.del_data(new_vacancies)
    assert len(csv_saver.get_data()) == 2

    csv_saver.del_data(new_vacancies)
    assert len(csv_saver.get_data()) == 2

    csv_saver.del_data()
    assert len(csv_saver.get_data()) == 0
    assert CSVWriter(path_file).get_data() == []

    os.remove(path_file)
