from typing import Any
from unittest.mock import Mock, patch

from src.head_hunter_api import HeadHunterAPI


def test_head_hunter_api_init(hh_api: HeadHunterAPI) -> None:
    assert hh_api.url == "https://api.hh.ru/vacancies"
    assert hh_api.params == dict()


@patch("src.head_hunter_api.requests.get")
def test_connect_to_api(mock_get: Mock, hh_api: HeadHunterAPI, response_api: dict, capsys: Any) -> None:
    mock_get.return_value.json.return_value = response_api
    mock_get.return_value.status_code = 200
    assert hh_api._connect_to_api() == response_api

    mock_get.return_value.json.return_value = response_api
    mock_get.return_value.status_code = 500
    assert hh_api._connect_to_api() == dict()
    message = capsys.readouterr()
    assert message.out.strip() == "Возникла ошибка при подключении к внешнему сервису API"


@patch("src.head_hunter_api.HeadHunterAPI._connect_to_api")
def test_get_vacancies(
    mock_get: Mock, hh_api: HeadHunterAPI, response_api: dict, list_vacancies_1: list, capsys: Any
) -> None:
    mock_get.return_value = response_api
    assert hh_api.get_vacancies("Python", 2) == list_vacancies_1
    assert hh_api.params["text"] == "Python"
    assert hh_api.params["per_page"] == 2

    assert hh_api.get_vacancies("Python") == list_vacancies_1
    assert hh_api.params["per_page"] == 100

    mock_get.return_value = {}
    assert hh_api.get_vacancies("Python", 2) == []
    message = capsys.readouterr()
    assert message.out.strip() == "Вакансии не найдены"
