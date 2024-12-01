
import requests

class HH:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        """Конструктор класса"""
        self.url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {"per_page": 100, "page": 0, "only_with_salary": True}
        self.employers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def get_employers(self):
        """Загрузка информации о работодателях"""
        return [requests.get(f"{self.url}employers/{employer_id}").json() for employer_id in self.employers]

    def get_vacancies(self):
        """Загрузка вакансий"""
        vacancies = []
        for employer_id in self.employers:
            self.params["employer_id"] = employer_id
            response = requests.get(f"{self.url}vacancies", headers=self.headers, params=self.params)
            vacancies.extend(response.json().get('items', []))
        return vacancies
