import psycopg2

def create_db(db_name: str, params):
    """Создание базы данных."""
    with psycopg2.connect(dbname='postgres', **params) as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")

    # Создание таблиц в новой базе данных
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INTEGER PRIMARY KEY,
                    employer_name TEXT NOT NULL,
                    employer_area TEXT NOT NULL,
                    url TEXT,
                    open_vacancies INTEGER
                )
            """)
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id INTEGER,
                    vacancy_name VARCHAR,
                    vacancy_area VARCHAR,
                    salary INTEGER,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_url VARCHAR
                )
            """)

def save_info_db(employers: list[dict], vacancies: list[dict], db_name: str, params: dict):
    """Сохранение данных о работодателях и вакансиях в базу данных."""
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute("""
                    INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    employer['id'],
                    employer['name'],
                    employer['area']['name'],
                    employer['alternate_url'],
                    employer['open_vacancies']
                ))

            for vacancy in vacancies:
                salary_from = vacancy['salary']['from'] if vacancy.get('salary') else 0
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['area']['name'],
                    salary_from,
                    vacancy['employer']['id'],
                    vacancy['alternate_url']
                ))
