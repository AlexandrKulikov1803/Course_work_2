import os

import pandas as pd

from src.file_writer import FileWriter
from src.vacancy import Vacancy


class XLSXWriter(FileWriter):
    """Абстрактный класс для работы с xlsx-файлами"""

    __path_xlsx_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.xlsx")

    def __init__(self, path_file: str | None = default_path_file):
        """Конструктор для имени xlsx-файла"""

        self.__path_xlsx_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из xlsx-файла"""

        try:
            df = pd.read_excel(self.__path_xlsx_file)
            list_vacancies_dict = df.to_dict(orient="records")

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)
            if not list_vacancies_obj:
                print("Файл пустой")  # логирование
                return []
            elif len(list_vacancies_dict[0]) > 4:
                print("Файл содержит некорректные данные")  # логирование
                return []
            else:
                return list_vacancies_obj

        except FileNotFoundError:
            print("Файл не найден")  # логирование
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в xlsx-файл"""

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

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных xlsx-файла"""

        if new_vacancies is None:
            df = pd.DataFrame({"name": [], "url": [], "salary": [], "experience": []})
            df.to_excel(self.__path_xlsx_file, index=False)
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

    @property
    def path_xlsx_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_xlsx_file
