from typing import Any

from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies, print_vacancies, get_vacancies_by_salary
from src.vacancy import Vacancy


def test_filter_vacancies(list_vacancies_2: list) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies_2)
    assert len(vacancies) == 8

    filtered_vacancies = filter_vacancies(vacancies, 0)
    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].name == "Python Developer"
    assert filtered_vacancies[1].name == "HTML Developer"

    filtered_vacancies = filter_vacancies(vacancies, 2)
    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].name == "Java Developer"
    assert filtered_vacancies[1].name == "PHP Developer"

    filtered_vacancies = filter_vacancies(vacancies, 4)
    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].name == "Kotlin Developer"
    assert filtered_vacancies[1].name == "C# Developer"

    filtered_vacancies = filter_vacancies(vacancies, 7)
    assert len(filtered_vacancies) == 2
    assert filtered_vacancies[0].name == "JavaScript Developer"
    assert filtered_vacancies[1].name == "Go Developer"


def test_get_vacancies_by_salary(list_vacancies_2: list) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies_2)
    ranged_vacancies = get_vacancies_by_salary(vacancies, '150000 -320000')

    assert len(ranged_vacancies) == 4

def test_sort_vacancies(list_vacancies_2: list) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies_2)
    sorted_vacancies = sort_vacancies(vacancies)

    assert sorted_vacancies[0].name == "Python Developer"
    assert sorted_vacancies[1].name == "HTML Developer"
    assert sorted_vacancies[2].name == "Java Developer"
    assert sorted_vacancies[3].name == "PHP Developer"
    assert sorted_vacancies[4].name == "Kotlin Developer"
    assert sorted_vacancies[5].name == "C# Developer"
    assert sorted_vacancies[6].name == "JavaScript Developer"
    assert sorted_vacancies[7].name == "Go Developer"


def test_get_top_vacancies(list_vacancies_2: list) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies_2)
    assert get_top_vacancies(vacancies, 8) == vacancies
    assert get_top_vacancies(vacancies, 10) == vacancies


def test_print_vacancies(list_vacancies_1: list, capsys: Any) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies_1)
    print_vacancies(vacancies)
    message = capsys.readouterr()
    assert message.out.strip() == ("name: Middle Backend-разработчик (Python), "
                                   "url: https://api.hh.ru/vacancies/124016761?host=hh.ru, "
                                   "salary: Не указана, "
                                   "experience: От 3 до 6 лет\n"
                                   "name: Backend-разработчик, "
                                   "url: https://api.hh.ru/vacancies/124008575?host=hh.ru, "
                                   "salary: 40000, "
                                   "experience: От 3 до 6 лет")
