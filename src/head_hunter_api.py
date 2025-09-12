import requests

from src.base_api import BaseApi


class HeadHunterAPI(BaseApi):
    """Класс для работы с API HeadHunter"""

    __url: str
    __params: dict

    def __init__(self) -> None:
        """Конструктор для API hh.ru"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__params = dict()

    def _connect_to_api(self) -> dict:
        """Метод подключения к API hh.ru"""

        response = requests.get(self.__url, params=self.__params)
        if response.status_code != 200:
            print("Возникла ошибка при подключении к внешнему сервису API")  # логирование
            return dict()
        else:
            return response.json()

    def get_vacancies(self, keyword: str, per_page: int = 100) -> list:
        """Метод получения вакансий"""

        self.__params["text"] = keyword
        self.__params["per_page"] = per_page
        list_vacancies = self._connect_to_api().get("items")
        if list_vacancies is None:
            print("Вакансии не найдены")  # логирование
            return []
        else:
            return list_vacancies

    @property
    def url(self) -> str:
        """Метод, который возвращает url"""

        return self.__url

    @property
    def params(self) -> dict:
        """Метод, который возвращает путь параметры api-запроса"""

        return self.__params
