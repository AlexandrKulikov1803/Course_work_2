import json
import os
from json import JSONDecodeError

from src.file_writer import FileWriter
from src.vacancy import Vacancy


class JSONWriter(FileWriter):
    """Абстрактный класс для работы с json-файлами"""

    __path_json_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.json")

    def __init__(self, path_file: str | None = None) -> None:
        """Конструктор для имени json-файла"""

        if path_file == "" or path_file is None:
            self.__path_json_file = self.default_path_file
        else:
            self.__path_json_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из json-файла"""

        try:
            with open(self.__path_json_file, "r", encoding="utf-8") as file:
                list_vacancies_dict = json.load(file)

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)
            return list_vacancies_obj

        except FileNotFoundError:
            print("Файл не найден")  # логирование
            return []

        except JSONDecodeError:
            if os.path.getsize(self.__path_json_file) == 0:
                print("Файл пустой")  # логирование
            else:
                print("Файл содержит некорректные данные")  # логирование
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в json-файл"""

        vacancies = self.get_data()

        if isinstance(new_vacancies, Vacancy):
            if new_vacancies not in vacancies:
                vacancies.append(new_vacancies)

        elif isinstance(new_vacancies, list):
            for new_vacancy in new_vacancies:
                if new_vacancy not in vacancies:
                    vacancies.append(new_vacancy)

        with open(self.__path_json_file, "w", encoding="utf-8") as file:
            list_vacancies = []
            for vacancy in vacancies:
                vacancy_to_add = {
                    "name": vacancy.name,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "experience": vacancy.experience,
                }
                list_vacancies.append(vacancy_to_add)
            json.dump(list_vacancies, file, ensure_ascii=False)

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных json-файла"""

        if new_vacancies is None:
            file = open(self.__path_json_file, "w")
            file.close()
        else:
            vacancies = self.get_data()

            if isinstance(new_vacancies, Vacancy):
                if new_vacancies in vacancies:
                    vacancies.remove(new_vacancies)

            elif isinstance(new_vacancies, list):
                for new_vacancy in new_vacancies:
                    if new_vacancy in vacancies:
                        vacancies.remove(new_vacancy)

            with open(self.__path_json_file, "w", encoding="utf-8") as file:
                list_vacancies = []
                for vacancy in vacancies:
                    vacancy_to_add = {
                        "name": vacancy.name,
                        "url": vacancy.url,
                        "salary": vacancy.salary,
                        "experience": vacancy.experience,
                    }
                    list_vacancies.append(vacancy_to_add)
                json.dump(list_vacancies, file, ensure_ascii=False)

    @property
    def path_json_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_json_file
