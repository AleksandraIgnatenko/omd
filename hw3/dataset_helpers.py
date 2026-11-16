from typing import List, Dict, Any, Callable, Tuple, Set


def count_missing_values(data: List[Dict[str, Any]], field: str) -> int:
    """
    Подсчитывает количество пропусков
    (None или отсутствующих ключей) в указанном поле.

    Args:
        data: список словарей
        field: имя поля

    Returns:
        количество пропусков
    """
    missing = 0
    for record in data:
        value = record.get(field)
        if value is None:
            missing += 1
    return missing


def count_records(data: List[Dict[str, Any]]) -> int:
    """
    Возвращает общее количество записей.

    Args:
        data: список словарей

    Returns:
        int количество записей
    """
    return len(data)


def get_all_unique_fields(data: List[Dict[str, Any]]) -> List[str]:
    """
    Возвращает все уникальные поля из списка словарей.

    Args:
        data: список словарей

    Returns:
        список уникальных имен полей
    """
    fields: Set[str] = set()
    for record in data:
        fields.update(record.keys())
    return sorted(list(fields))


def filter_data(
    data: List[Dict[str, Any]],
    condition: Callable[[Dict[str, Any]], bool]
) -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей, оставляя только те записи,
    которые удовлетворяют заданному условию.

    Args:
        data (List[Dict[str, Any]]): Исходный список словарей с данными.
        condition (Callable[[Dict[str, Any]], bool]): Функция,
            которая принимает словарь и возвращает True,
            если запись должна быть сохранена,
            и False в противном случае.

    Returns:
        List[Dict[str, Any]]: Новый список словарей,
        содержащий только отфильтрованные записи.
    """
    return [record for record in data if condition(record)]


def group_by_attributes(
    data: List[Dict[str, Any]],
    attributes: List[str]
) -> Dict[Tuple, List[Dict[str, Any]]]:
    """
    Группирует список словарей по значениям указанных атрибутов.

    Args:
        data (List[Dict[str, Any]]): Исходный список словарей с данными.
        attributes (List[str]): Список имен ключей (атрибутов), по которым
            необходимо сгруппировать данные.

    Returns:
        Dict[Tuple, List[Dict[str, Any]]]: Словарь, где:
            - ключ (Tuple): кортеж значений атрибутов для данной группы
            - значение (List[Dict[str, Any]]): список словарей (записей),
              принадлежащих этой группе.
    """
    groups: Dict[Tuple, List[Dict[str, Any]]] = {}
    for record in data:
        key = tuple(record.get(attr) for attr in attributes)
        if key not in groups:
            groups[key] = []
        groups[key].append(record)
    return groups


def apply_aggregation(
    data: List[Dict[str, Any]],
    field: str,
    agg_func: Callable[[List[Any]], Any]
) -> Any:
    """
    Извлекает значения из указанного поля всех словарей
    и применяет к ним агрегирующую функцию.

    Args:
        data (List[Dict[str, Any]]): Исходный список словарей с данными.
        field (str): Имя ключа (поля), значения которого будут агрегированы.
        agg_func (Callable[[List[Any]], Any]): Функция агрегации,
            которая принимает список значений
            и возвращает агрегированный результат.

    Returns:
        Any: Результат применения агрегирующей функции. Возвращает None,
        если в данных нет записей или все значения
        для указанного поля равны None.
    """
    values = [
        record.get(field) for record in data
        if record.get(field) is not None
    ]
    if not values:
        return None
    return agg_func(values)
