import os

import pandas as pd

from logging_config import setup_logger
from src.file_writer import FileWriter
from src.vacancy import Vacancy

path_logger = os.path.join(os.getcwd(), "log")
os.makedirs(path_logger, exist_ok=True)
logger = setup_logger("xlsx_writer", f"{path_logger}/xlsx_writer.txt")


class XLSXWriter(FileWriter):
    """Абстрактный класс для работы с xlsx-файлами"""

    __path_xlsx_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.xlsx")

    def __init__(self, path_file: str | None = None) -> None:
        """Конструктор для имени xlsx-файла"""

        if path_file == "" or path_file is None:
            self.__path_xlsx_file = self.default_path_file
        else:
            self.__path_xlsx_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из xlsx-файла"""

        try:
            logger.info("Началось считывание данных из xlsx-файла")

            df = pd.read_excel(self.__path_xlsx_file)
            list_vacancies_dict = df.to_dict(orient="records")

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)
            if not list_vacancies_obj:
                logger.error("Файл пустой")
                return []
            elif len(list_vacancies_dict[0]) > 4:
                logger.error("Файл содержит некорректные данные")
                return []
            else:
                logger.info("Данные из xlsx-файла успешно получены")
                return list_vacancies_obj

        except FileNotFoundError:
            logger.error("Файл не найден")
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в xlsx-файл"""

        logger.info("Началось добавление данных в xlsx-файл")

        vacancies = self.get_data()

        if isinstance(new_vacancies, Vacancy):
            if new_vacancies not in vacancies:
                vacancies.append(new_vacancies)

        elif isinstance(new_vacancies, list):
            for new_vacancy in new_vacancies:
                if new_vacancy not in vacancies:
                    vacancies.append(new_vacancy)

        list_vacancies = []
        for vacancy in vacancies:
            vacancy_to_add = {
                "name": vacancy.name,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "experience": vacancy.experience,
            }
            list_vacancies.append(vacancy_to_add)

        df_vacancies = pd.DataFrame(list_vacancies)
        df_vacancies.to_excel(self.__path_xlsx_file, index=False)

        logger.info("Данные в xlsx-файл успешно добавлены")

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных xlsx-файла"""

        logger.info("Началось удаление данных из xlsx-файла")

        if new_vacancies is None:
            df = pd.DataFrame({"name": [], "url": [], "salary": [], "experience": []})
            df.to_excel(self.__path_xlsx_file, index=False)

            logger.info("Данные из xlsx-файла полностью удалены")
        else:
            vacancies = self.get_data()

            if isinstance(new_vacancies, Vacancy):
                if new_vacancies in vacancies:
                    vacancies.remove(new_vacancies)

            elif isinstance(new_vacancies, list):
                for new_vacancy in new_vacancies:
                    if new_vacancy in vacancies:
                        vacancies.remove(new_vacancy)

            list_vacancies = []
            for vacancy in vacancies:
                vacancy_to_add = {
                    "name": vacancy.name,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "experience": vacancy.experience,
                }
                list_vacancies.append(vacancy_to_add)

            df_vacancies = pd.DataFrame(list_vacancies)
            df_vacancies.to_excel(self.__path_xlsx_file, index=False)

            logger.info("Вакансии из xlsx-файла успешно удалены")

    @property
    def path_xlsx_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_xlsx_file
