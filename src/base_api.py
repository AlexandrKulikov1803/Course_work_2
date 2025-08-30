from abc import ABC, abstractmethod


class BaseApi(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self):
        """Конструктор для API"""
        pass  # pragma: no cover

    @abstractmethod
    def _connect_to_api(self) -> dict:
        """Метод подключения к API"""
        pass  # pragma: no cover

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int) -> list:
        """Метод получения вакансий"""
        pass  # pragma: no cover
