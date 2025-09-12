import json
import os
from json import JSONDecodeError

from src.file_writer import FileWriter
from src.vacancy import Vacancy


class TXTWriter(FileWriter):
    """Абстрактный класс для работы с txt-файлами"""

    __path_txt_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.txt")

    def __init__(self, path_file: str | None = default_path_file):
        """Конструктор для имени txt-файла"""

        self.__path_txt_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из txt-файла"""

        try:
            with open(self.__path_txt_file, "r", encoding="utf-8") as file:
                text = file.read()
                list_vacancies_dict = json.loads(text)

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)
            return list_vacancies_obj

        except FileNotFoundError:
            print("Файл не найден")  # логирование
            return []

        except JSONDecodeError:
            if os.path.getsize(self.__path_txt_file) == 0:
                print("Файл пустой")  # логирование
            else:
                print("Файл содержит некорректные данные")  # логирование
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в txt-файл"""

        vacancies = self.get_data()

        if isinstance(new_vacancies, Vacancy):
            if new_vacancies not in vacancies:
                vacancies.append(new_vacancies)

        elif isinstance(new_vacancies, list):
            for new_vacancy in new_vacancies:
                if new_vacancy not in vacancies:
                    vacancies.append(new_vacancy)

        with open(self.__path_txt_file, "w", encoding="utf-8") as file:
            list_vacancies = []
            for vacancy in vacancies:
                vacancy_to_add = {
                    "name": vacancy.name,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "experience": vacancy.experience,
                }
                list_vacancies.append(vacancy_to_add)
            text = json.dumps(list_vacancies, ensure_ascii=False)
            file.write(text)

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных txt-файла"""

        if new_vacancies is None:
            file = open(self.__path_txt_file, "w")
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

            with open(self.__path_txt_file, "w", encoding="utf-8") as file:
                list_vacancies = []
                for vacancy in vacancies:
                    vacancy_to_add = {
                        "name": vacancy.name,
                        "url": vacancy.url,
                        "salary": vacancy.salary,
                        "experience": vacancy.experience,
                    }
                    list_vacancies.append(vacancy_to_add)
                text = json.dumps(list_vacancies, ensure_ascii=False)
                file.write(text)

    @property
    def path_txt_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_txt_file
