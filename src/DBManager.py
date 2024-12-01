import psycopg2

class DBManager:
    def __init__(self, db_name, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT companies.name, COUNT(vacancies.id) 
        FROM companies 
        LEFT JOIN vacancies ON companies.id = vacancies.company_id 
        GROUP BY companies.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary, vacancies.url 
        FROM vacancies 
        JOIN companies ON vacancies.company_id = companies.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = "SELECT AVG(salary) FROM vacancies;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary, vacancies.url 
        FROM vacancies 
        JOIN companies ON vacancies.company_id = companies.id 
        WHERE vacancies.salary > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        query = """
        SELECT companies.name, vacancies.name, vacancies.salary, vacancies.url 
        FROM vacancies 
        JOIN companies ON vacancies.company_id = companies.id 
        WHERE vacancies.name LIKE %s;
        """
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db_manager = DBManager(db_name="your_db_name", user="your_user", password="your_password", host="localhost",
                           port="5432")

    print("Companies and vacancies count:")
    print(db_manager.get_companies_and_vacancies_count())

    print("All vacancies:")
    print(db_manager.get_all_vacancies())

    print("Average salary:")
    print(db_manager.get_avg_salary())

    print("Vacancies with higher salary than average:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("Vacancies with keyword 'python':")
    print(db_manager.get_vacancies_with_keyword("python"))

    db_manager.close()
