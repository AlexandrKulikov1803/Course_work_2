import os
from typing import Any

import requests

from logging_config import setup_logger
from src.base_api import BaseApi

path_logger = os.path.join(os.getcwd(), "log")
os.makedirs(path_logger, exist_ok=True)
logger = setup_logger("head_hunter_api", f"{path_logger}/head_hunter_api.txt")


class HeadHunterAPI(BaseApi):
    """Класс для работы с API HeadHunter"""

    __url: str
    __params: dict

    def __init__(self) -> None:
        """Конструктор для API hh.ru"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__params = dict()

    def _connect_to_api(self) -> Any:
        """Метод подключения к API hh.ru"""

        logger.info("Началось подключение к API hh.ru")

        response = requests.get(self.__url, params=self.__params)
        if response.status_code != 200:
            logger.error("Возникла ошибка при подключении к внешнему сервису API")
            return {}
        else:
            logger.info("Подключение к внешнему сервису API прошло успешно")
            return response.json()

    def get_vacancies(self, keyword: str, per_page: int = 100) -> Any:
        """Метод получения вакансий"""

        logger.info("Началось получение вакансий")

        self.__params["text"] = keyword
        self.__params["per_page"] = per_page
        list_vacancies = self._connect_to_api().get("items")
        if list_vacancies is None:
            logger.error("Вакансии не найдены")
            return []
        else:
            logger.info("Вакансии успешно получены")
            return list_vacancies

    @property
    def url(self) -> str:
        """Метод, который возвращает url"""

        return self.__url

    @property
    def params(self) -> dict:
        """Метод, который возвращает путь параметры api-запроса"""

        return self.__params

a = HeadHunterAPI()
print(a._connect_to_api())
print(type(a._connect_to_api()))