from typing import List, Dict, Any, Callable, Tuple, Union


def extract_nested_value(obj: Any, keys: List[str]) -> Any:
    """
    Извлекает значение из вложенной структуры словарей
    по последовательности ключей.

    Args:
        obj (Any): Исходный объект, из которого извлекается значение.
        keys (List[str]): Список ключей, определяющих путь к целевому значению.

    Returns:
        Any: Значение по указанному пути или None, если путь неверный
        (ключ отсутствует, объект не словарь или встретился None).
    """
    for key in keys:
        if obj is None:
            return None
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj


def process_dictionary_with_config(
    dictionary: Dict[str, Any],
    config: Dict[str, Union[List[str], Tuple[List[str], Callable[[Any], Any]]]]
) -> Dict[str, Any]:
    """
    Обрабатывает один словарь согласно заданной конфигурации извлечения полей.

    Args:
        dictionary (Dict[str, Any]): Исходный словарь для обработки.
        config (Dict[str, Union[List[str], Tuple[List[str], Callable]]]):
            Конфигурация обработки.

    Returns:
        Dict[str, Any]: Новый словарь с извлечёнными и, при необходимости,
        преобразованными значениями. Если значение по пути равно None,
        функция-преобразователь не применяется,
        и в результат записывается None.
    """
    res: Dict[str, Any] = {}
    for attr_name, rule in config.items():
        if isinstance(rule, tuple):
            path, func = rule
            value = extract_nested_value(dictionary, path)
            res[attr_name] = func(value) if value is not None else None
        else:
            path = rule
            res[attr_name] = extract_nested_value(dictionary, path)
    return res


def process_list_of_dicts_with_config(
    list_of_dicts: List[Dict[str, Any]],
    config: Dict[str, Union[List[str], Tuple[List[str], Callable[[Any], Any]]]]
) -> List[Dict[str, Any]]:
    """
    Применяет обработку конфигурацией ко всему списку словарей.

    Args:
        list_of_dicts (List[Dict[str, Any]]): Исходный список словарей.
        config (Dict[str, Union[List[str], Tuple[List[str], Callable]]]):
            Конфигурация обработки.

    Returns:
        List[Dict[str, Any]]: Новый список словарей,
        каждый из которых обработан
        согласно конфигурации. Возвращает пустой список,
        если входной список пуст.
    """
    if not list_of_dicts:
        return []
    return [process_dictionary_with_config(d, config) for d in list_of_dicts]


def create_processor(
    config: Dict[
        str, Union[List[str], Tuple[List[str], Callable[[Any], Any]]]
    ],
    list_processor: bool = False
) -> Callable[[Any], Any]:
    """
    Фабрика процессоров: создаёт
    и возвращает функцию-обработчик данных
    на основе заданной конфигурации.

    Args:
        config (Dict[str, Union[List[str], Tuple[List[str], Callable]]]):
            Конфигурация обработки полей.
        list_processor (bool, optional):
            Если True, возвращается процессор для списка словарей.
            Если False (по умолчанию) — для одиночного словаря.

    Returns:
        Callable[[Any], Any]:
        Функция-процессор, принимающая данные и возвращающая
        обработанный результат (словарь или список словарей).
    """
    if list_processor:
        return lambda data: process_list_of_dicts_with_config(data, config)
    return lambda data: process_dictionary_with_config(data, config)
