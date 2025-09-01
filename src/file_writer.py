from abc import ABC, abstractmethod

from src.vacancy import Vacancy


class FileWriter(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def __init__(self, path_file: str | None) -> None:
        """Конструктор для имени файла"""
        pass  # pragma: no cover

    @abstractmethod
    def get_data(self) -> list:
        """Метод получения данных из файла"""
        pass  # pragma: no cover

    @abstractmethod
    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в файл"""
        pass  # pragma: no cover

    @abstractmethod
    def del_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод удаления данных файла"""
        pass  # pragma: no cover
