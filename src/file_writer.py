from abc import ABC, abstractmethod

class FileWriter(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def __init__(self) -> None:
        """Конструктор для имени файла"""
        pass  # pragma: no cover

    @abstractmethod
    def get_data(self) -> list:
        """Метод получения данных из файла"""
        pass  # pragma: no cover

    @abstractmethod
    def add_data(self) -> None:
        """Метод добавления данных в файл"""
        pass  # pragma: no cover

    @abstractmethod
    def del_data(self) -> None:
        """Метод удаления данных файла"""
        pass  # pragma: no cover