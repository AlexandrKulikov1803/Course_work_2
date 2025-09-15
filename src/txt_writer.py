import json
import os
from json import JSONDecodeError

from logging_config import setup_logger
from src.file_writer import FileWriter
from src.vacancy import Vacancy

path_logger = os.path.join(os.getcwd(), "log")
os.makedirs(path_logger, exist_ok=True)
logger = setup_logger("txt_writer", f"{path_logger}/txt_writer.txt")


class TXTWriter(FileWriter):
    """Абстрактный класс для работы с txt-файлами"""

    __path_txt_file: str

    directory = os.getcwd()
    default_path_file = os.path.join(directory, "data", "vacancies.txt")

    def __init__(self, path_file: str | None = None) -> None:
        """Конструктор для имени txt-файла"""

        if path_file == "" or path_file is None:
            self.__path_txt_file = self.default_path_file
        else:
            self.__path_txt_file = path_file

    def get_data(self) -> list:
        """Метод получения данных из txt-файла"""

        try:
            logger.info("Началось считывание данных из txt-файла")

            with open(self.__path_txt_file, "r", encoding="utf-8") as file:
                text = file.read()
                list_vacancies_dict = json.loads(text)

            list_vacancies_obj = Vacancy.cast_to_object_list(list_vacancies_dict)
            logger.info("Данные из txt-файла успешно получены")

            return list_vacancies_obj

        except FileNotFoundError:
            logger.error("Файл не найден")
            return []

        except JSONDecodeError:
            if os.path.getsize(self.__path_txt_file) == 0:
                logger.error("Файл пустой")
            else:
                logger.error("Файл содержит некорректные данные")
            return []

    def add_data(self, new_vacancies: Vacancy | list[Vacancy]) -> None:
        """Метод добавления данных в txt-файл"""

        logger.info("Началось добавление данных в txt-файл")

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

        logger.info("Данные в txt-файл успешно добавлены")

    def del_data(self, new_vacancies: Vacancy | list[Vacancy] | None = None) -> None:
        """Метод удаления данных txt-файла"""

        logger.info("Началось удаление данных из txt-файла")

        if new_vacancies is None:
            file = open(self.__path_txt_file, "w")
            file.close()

            logger.info("Данные из txt-файла полностью удалены")
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

            logger.info("Вакансии из txt-файла успешно удалены")

    @property
    def path_txt_file(self) -> str:
        """Метод, который возвращает путь к файлу"""

        return self.__path_txt_file
