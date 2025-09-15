import os
import re

from logging_config import setup_logger

path_logger = os.path.join(os.getcwd(), "log")
os.makedirs(path_logger, exist_ok=True)
logger = setup_logger("utils", f"{path_logger}/utils.txt")


def filter_vacancies(vacancies_list: list, filter_experience: int) -> list:
    """Функция, фильтрующая список вакансий по опыту работы"""

    logger.info("Началась фильтрация списка вакансий по опыту работы")

    pattern_1 = re.compile(r"От \d года до \d лет")
    pattern_2 = re.compile(r"От \d до \d лет")
    pattern_3 = re.compile(r"Более \d лет")

    filtered_vacancies = []
    for vacancy in vacancies_list:
        experience = vacancy.experience

        if pattern_1.search(experience) and 1 <= filter_experience <= 3:
            filtered_vacancies.append(vacancy)

        elif pattern_2.search(experience) and 3 <= filter_experience <= 6:
            filtered_vacancies.append(vacancy)

        elif pattern_3.search(experience) and 6 <= filter_experience:
            filtered_vacancies.append(vacancy)

        elif experience == "Нет опыта" and filter_experience == 0:
            filtered_vacancies.append(vacancy)

    logger.info("Фильтрация успешно завершена")
    return filtered_vacancies


def get_vacancies_by_salary(vacancies_list: list, salary_range: str) -> list:
    """Функция, которая возвращает список вакансий в диапазоне заработной платы"""

    logger.info("Началась фильтрация списка вакансий по заработной плате")

    salary_range = salary_range.replace(" ", "")
    salary_range_list = salary_range.split("-")
    min_value = int(salary_range_list[0])
    max_value = int(salary_range_list[1])

    vacancies = skip_vacancies_without_salary(vacancies_list)
    filtered_vacancies = [vacancy for vacancy in vacancies if min_value <= vacancy.salary <= max_value]

    logger.info("Фильтрация успешно завершена")
    return filtered_vacancies


def sort_vacancies(vacancies_list: list) -> list:
    """Функция, которая сортирует список вакансий по заработной плате"""

    logger.info("Началась сортировка списка вакансий по заработной плате")

    vacancies = skip_vacancies_without_salary(vacancies_list)

    logger.info("Сортировка успешно завершена")
    return sorted(vacancies, key=lambda vacancy: vacancy.salary)


def get_top_vacancies(vacancies_list: list, top_n: int) -> list:
    """Функция, которая возвращает топ N вакансий"""

    logger.info("Начался отсчёт топ N вакансий")

    top_vacancies = []
    if len(vacancies_list) >= top_n:
        top_vacancies.extend(vacancies_list[0:top_n])
    else:
        top_vacancies.extend(vacancies_list)

    logger.info("Отчёт топ N вакансий успешно завершён")
    return top_vacancies


def print_vacancies(vacancies_list: list) -> None:
    """Функция для вывода топ N вакансий"""

    for vacancy in vacancies_list:
        print(vacancy)

    logger.info("Выведено топ N вакансий")


def skip_vacancies_without_salary(vacancies_list: list) -> list:
    """Функция, которая позволяет пропустить вакансии без указанной заработной платы"""

    return [vacancy for vacancy in vacancies_list if isinstance(vacancy.salary, int)]
