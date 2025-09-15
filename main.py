import sys


from src.csv_writer import CSVWriter
from src.file_writer import FileWriter
from src.head_hunter_api import HeadHunterAPI
from src.json_writer import JSONWriter
from src.txt_writer import TXTWriter
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy
from src.xlsx_writer import XLSXWriter


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""

    hh_api = HeadHunterAPI()

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))

    hh_vacancies = hh_api.get_vacancies(search_query, 100)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    filter_experience = int(input("Введите ваш опыт работы: "))  # Пример: 5
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000
    print()

    filtered_vacancies = filter_vacancies(vacancies_list, filter_experience)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)

    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

    record = input("\nХотите получить/записать/удалить вакансии из файла (да/нет)? ")

    if record == "да":
        path_file = input("Укажите расположение файла (путь файла по умолчанию С:/папка_проекта/data/vacancies.*): ")

        print(
            """Выберите расширение файла:
    1. Файл с расширением json
    2. Файл с расширением txt
    3. Файл с расширением csv
    4. Файл с расширением xlsx"""
        )

        file_extension = int(input())

        print(
            """Выберите необходимый действие:
    1. Получить информацию о записанных вакансиях
    2. Записать информацию о вакансиях
    3. Удалить информацию о вакансиях
    4. Очистить файл"""
        )

        option = int(input())

        writer: FileWriter
        if file_extension == 1:
            writer = JSONWriter(path_file)
        elif file_extension == 2:
            writer = TXTWriter(path_file)
        elif file_extension == 3:
            writer = CSVWriter(path_file)
        elif file_extension == 4:
            writer = XLSXWriter(path_file)
        else:
            sys.exit()

        if option == 1:
            vacancies = writer.get_data()
            for vacancy in vacancies:
                print(vacancy)
        elif option == 2:
            writer.add_data(top_vacancies)
        elif option == 3:
            writer.del_data(top_vacancies)
        elif option == 4:
            writer.del_data()


if __name__ == "__main__":
    user_interaction()
