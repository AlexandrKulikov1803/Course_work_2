import os

import pandas
import pandas as pd

from logging_config import setup_logger
from src.file_writer import FileWriter
from src.vacancy import Vacancy

path_logger = os.path.join(os.getcwd(), "log")
os.makedirs(path_logger, exist_ok=True)
logger = setup_logger("csv_writer", f"{path_logger}/csv_writer.txt")


class CSVWriter(FileWriter):
    """Абстрактный класс для работы с csv-файлами"""

    __path_csv_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.csv")

    def __init__(self, path_file: str | None = None) -> None:
        """Конструктор для имени csv-файла"""

        if path_file == "" or path_file is None:
            self.__path_csv_file = self.default_path_file
        else:
            self.__path_csv_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из csv-файла"""

        try:
            logger.info("Началось считывание данных из csv-файла")

            df = pd.read_csv(self.__path_csv_file, delimiter=";", encoding="utf-8-sig")
            df["salary"] = df["salary"].fillna("Не указана")
            list_vacancies_dict = df.to_dict(orient="records")

            for vacancy in list_vacancies_dict:
                if vacancy["salary"] != "Не указана":
                    vacancy["salary"] = int(vacancy["salary"])

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)

            if not list_vacancies_obj:
                logger.error("Файл пустой")
                return []
            else:
                logger.info("Данные из csv-файла успешно получены")
                return list_vacancies_obj

        except FileNotFoundError:
            logger.error("Файл не найден")
            return []
        except pandas.errors.EmptyDataError:
            logger.error("Файл пустой")
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в csv-файл"""

        logger.info("Началось добавление данных в csv-файл")

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
        df_vacancies.to_csv(self.__path_csv_file, index=False, encoding="utf-8-sig", sep=";")

        logger.info("Данные в csv-файл успешно добавлены")

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных csv-файла"""

        logger.info("Началось удаление данных из csv-файла")

        if new_vacancies is None:
            df = pd.DataFrame({"name": [], "url": [], "salary": [], "experience": []})
            df.to_csv(self.__path_csv_file, index=False, encoding="utf-8-sig", sep=";")

            logger.info("Данные из csv-файла полностью удалены")
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
            df_vacancies.to_csv(self.__path_csv_file, index=False, encoding="utf-8-sig", sep=";")

            logger.info("Вакансии из csv-файла успешно удалены")

    @property
    def path_csv_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_csv_file
