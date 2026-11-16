from typing import Any, Dict, Union, Optional, Callable
from json_dict_processing import create_processor
from prizes_configs import prize_processor


def process_year(
    date_string: Optional[Union[str, Dict[str, Any]]]
) -> Optional[int]:
    """
    Извлекает год из строки даты или словаря с датой.

    Args:
        date_string (Optional[Union[str, Dict[str, Any]]]):
            Дата в виде строки
            Может быть None.

    Returns:
        Optional[int]: Год в виде целого числа или None,
        если извлечение невозможно.
    """
    if not date_string:
        return None

    if isinstance(date_string, dict):
        date_str = date_string.get('date') or date_string.get('year')
        if date_str is None:
            return None
    else:
        date_str = str(date_string)

    try:
        return int(date_str.split('-')[0])
    except (ValueError, IndexError):
        return None


CONFIG_PERSON: Dict[str, Any] = {
    'id': (['id'], int),
    'name': ['knownName', 'en'],
    'gender': ['gender'],
    'birth_year': (['birth', 'date'], process_year),
    'country_birth': ['birth', 'place', 'country', 'en'],
    'country_now': ['birth', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor())
}


CONFIG_ORG: Dict[str, Any] = {
    'id': (['id'], int),
    'name': ['orgName', 'en'],
    'founded_year': (['founded', 'date'], process_year),
    'country_founded': ['founded', 'place', 'country', 'en'],
    'country_now': ['founded', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], prize_processor())
}


def person_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Создаёт и возвращает процессор для обработки данных лауреата-человека.

    Returns:
        Callable[[Dict[str, Any]], Dict[str, Any]]: Функция-процессор,
        принимающая словарь данных и возвращающая обработанный словарь.
    """
    return create_processor(CONFIG_PERSON, list_processor=False)


def org_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Создаёт и возвращает процессор для обработки данных лауреата-организации.

    Returns:
        Callable[[Dict[str, Any]], Dict[str, Any]]: Функция-процессор,
        принимающая словарь данных и возвращающая обработанный словарь.
    """
    return create_processor(CONFIG_ORG, list_processor=False)
