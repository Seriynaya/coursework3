from src.api_headhunter import HH
from src.utils import get_config
from src.DBManager import DBManager
from src.db_create import create_db, save_info_db


def main():
    """Функция для взаимодействия с пользователем"""
    params = get_config()
    HH_instance = HH()

    # Загружаем данные
    create_db('hh_db', params)
    save_info_db(HH_instance.get_employers(), HH_instance.get_vacancies(), 'hh_db', params)

    db_manager = DBManager(params)

    menu = """
    Введите цифру для получения нужной информации
    1 - Завершить программу
    2 - Список всех вакансий.
    3 - Список всех компаний и их количество вакансий.
    4 - Средняя зарплата по вакансиям.
    5 - Вакансии с зарплатой выше средней.
    6 - Вакансии по ключевому слову.
    """

    while True:
        print(menu)
        user_input = input()

        if user_input == "1":
            print("Программа завершила работу")
            break

        if user_input == "2":
            result = db_manager.get_all_vacancies()
            print("Список всех вакансий:")
        elif user_input == "3":
            result = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий:")

        elif user_input == '4':
            result = db_manager.get_avg_salary()
            print("Средняя зарплата по вакансиям:")
            print(result)
            continue
        elif user_input == "5":
            result = db_manager.get_vacancies_with_higher_salary()
            print("Вакансии с зарплатой выше средней:")
        elif user_input == "6":
            user_word = input("Введите ключевое слово\n").lower()
            result = db_manager.get_vacancies_with_keyword(user_word)
            print("Вакансии по ключевому слову:")
        else:
            print("Неверный ввод, попробуйте снова.")
            continue

        # Выводим результат
        for i in result:
            print(i)


if __name__ == '__main__':
    main()
