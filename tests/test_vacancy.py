import pytest

from src.vacancy import Vacancy


def test_vacancy_init(vacancy_1: Vacancy) -> None:
    assert vacancy_1.name == "Python Developer"
    assert vacancy_1.url == "https://hh.ru/vacancy/123456"
    assert vacancy_1.salary == 100000
    assert vacancy_1.experience == "3 года"

    assert len(Vacancy.all_vacancies) == 1


def test_cast_to_object_list(list_vacancies: list) -> None:
    vacancies = Vacancy.cast_to_object_list(list_vacancies)

    assert vacancies[0].name == "Middle Backend-разработчик (Python)"
    assert vacancies[0].url == "https://api.hh.ru/vacancies/124016761?host=hh.ru"
    assert vacancies[0].salary == "Не указана"
    assert vacancies[0].experience == "От 3 до 6 лет"

    assert vacancies[1].name == "Backend-разработчик"
    assert vacancies[1].url == "https://api.hh.ru/vacancies/124008575?host=hh.ru"
    assert vacancies[1].salary == 40000
    assert vacancies[1].experience == "От 3 до 6 лет"

    with pytest.raises(IndexError):
        print(vacancies[2])

    assert len(Vacancy.all_vacancies) == 3


@pytest.mark.parametrize(
    "salary, expected_result",
    [
        (None, "Не указана"),
        (100000, 100000),
        ({"from": 100000, "to": None, "currency": "RUR", "gross": False}, 100000),
        ({"from": None, "to": None, "currency": "RUR", "gross": False}, "Не указана"),
    ],
)
def test_validation_by_salary(salary: None | int | dict, expected_result: str | int) -> None:
    assert Vacancy._validation_by_salary(salary) == expected_result


@pytest.mark.parametrize(
    "experience, expected_result",
    [
        (None, "Нет опыта"),
        ("От 1 года до 3 лет", "От 1 года до 3 лет"),
        ({"id": "between3And6", "name": "От 3 до 6 лет"}, "От 3 до 6 лет"),
    ],
)
def test_validation_by_experience(experience: None | str | dict, expected_result: str) -> None:
    assert Vacancy._validation_by_experience(experience) == expected_result


def test_vacancy_ge(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    assert vacancy_1 >= vacancy_2
    assert not vacancy_2 >= vacancy_1


def test_vacancy_le(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    assert vacancy_2 <= vacancy_1
    assert not vacancy_1 <= vacancy_2


def test_vacancy_eq(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    assert vacancy_1 == vacancy_1
    assert not vacancy_1 == vacancy_2
    assert not vacancy_1 == 1
