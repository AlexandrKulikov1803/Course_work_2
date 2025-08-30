class Vacancy:
    __slots__ = ("name", "url", "salary", "experience")

    name: str
    url: str
    salary: str | int
    experience: str
    all_vacancies: list = []

    def __init__(
        self, name: str, url: str, salary: None | int | dict = None, experience: None | str | dict = None
    ) -> None:
        """Конструктор для вакансии"""

        self.name = name
        self.url = url
        self.salary = Vacancy._validation_by_salary(salary)
        self.experience = Vacancy._validation_by_experience(experience)

        Vacancy.all_vacancies.append(self)

    @classmethod
    def cast_to_object_list(cls, list_vacancies_json: list) -> list:
        """Метод преобразования набора данных из JSON в список объектов"""

        list_vacancies_obj = []

        for vacancy in list_vacancies_json:
            name = vacancy["name"]
            url = vacancy["url"]
            salary = vacancy["salary"]
            experience = vacancy["experience"]
            vacancy_obj = cls(name, url, salary, experience)
            list_vacancies_obj.append(vacancy_obj)

        return list_vacancies_obj

    @staticmethod
    def _validation_by_salary(salary: None | int | dict) -> str | int:
        """Метод для валидация по заработной плате"""

        if isinstance(salary, int):
            return salary
        elif isinstance(salary, dict) and salary["from"] is not None:
            return salary["from"]
        else:
            return "Не указана"

    @staticmethod
    def _validation_by_experience(experience: None | str | dict) -> str:
        """Метод для валидация по опыту работы"""

        if experience is None:
            return "Нет опыта"
        elif isinstance(experience, str):
            return experience
        elif isinstance(experience, dict):
            return experience["name"]

    def __ge__(self, other) -> bool:
        """Метод для операции сравнения «больше или равно»."""

        return self.salary >= other.salary

    def __le__(self, other) -> bool:
        """Метод для операции сравнения «меньше или равно»."""

        return self.salary <= other.salary

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            return False
        else:
            return (
                self.name == other.name
                and self.url == other.url
                and self.salary == other.salary
                and self.experience == other.experience
            )


if __name__ == "__main__":
    vacancy = Vacancy("Python Developer", "https://...", 100000, "От 1 года до 2 лет")
    print(vacancy.experience)
