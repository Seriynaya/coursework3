from configparser import ConfigParser

def get_config(filename="db.ini", section="postgres"):
    """Получение словаря с данными для подключения к БД."""
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise Exception(f'Section {section} not found in {filename}.')

    return {param[0]: param[1] for param in parser.items(section)}
