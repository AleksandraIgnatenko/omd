from typing import List, Any, Dict, Optional


def calc_mean(values: List[Any]) -> Optional[float]:
    """
    Расчет среднего арифметического значения.

    Args:
        values (List[Any]): Список числовых значений.

    Returns:
        Optional[float]: Среднее значение. Возвращает None, если список пуст.
    """
    if not values:
        return None
    return sum(values) / len(values)


def calc_median(values: List[Any]) -> Optional[float]:
    """
    Расчет медианного значения.

    Args:
        values (List[Any]): Список числовых значений.

    Returns:
        Optional[float]: Медиана списка. Возвращает None, если список пуст.
    """
    if not values:
        return None
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid-1] + sorted_values[mid]) / 2
    else:
        return sorted_values[mid]


def calc_max(values: List[Any]) -> Optional[float]:
    """
    Расчет максимального значения в списке.

    Args:
        values (List[Any]): Список числовых значений.

    Returns:
        Optional[float]: Максимальное значение.
        Возвращает None, если список пуст.
    """
    if not values:
        return None
    return max(values)


def calc_min(values: List[Any]) -> Optional[float]:
    """
    Расчет минимального значения в списке.

    Args:
        values (List[Any]): Список числовых значений.

    Returns:
        Optional[float]: Минимальное значение.
        Возвращает None, если список пуст.
    """
    if not values:
        return None
    return min(values)


def calc_count(values: List[Any]) -> int:
    """
    Подсчет количества элементов в списке.

    Args:
        values (List[Any]): Список любых значений.

    Returns:
        int: Количество элементов в списке.
    """
    return len(values)


def calc_sum(values: List[Any]) -> Any:
    """
    Расчет суммы значений в списке.

    Args:
        values (List[Any]): Список числовых значений.

    Returns:
        Any: Сумма элементов списка. Возвращает 0, если список пуст.
    """
    if not values:
        return 0
    return sum(values)


def get_top_n(
    data: List[Dict[str, Any]],
    sort_key: str,
    n: int,
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N записей из списка словарей,
    отсортированных по указанному ключу.

    Args:
        data (List[Dict[str, Any]]): Исходный список словарей с данными.
        sort_key (str): Ключ словаря, по которому производится сортировка.
        n (int): Количество возвращаемых лучших записей.
        reverse (bool, optional): Флаг сортировки.

    Returns:
        List[Dict[str, Any]]: Список из топ-N словарей,
        отфильтрованный от записей с None по ключу sort_key.
    """
    valid_data = [d for d in data if d.get(sort_key) is not None]
    sorted_data = sorted(
        valid_data,
        key=lambda x: x[sort_key],
        reverse=reverse
    )
    return sorted_data[:n]
