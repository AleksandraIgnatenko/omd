from typing import List, Dict, Any, Callable


def add_computed_field(
    data: List[Dict[str, Any]],
    new_field: str,
    compute_func: Callable[[Dict[str, Any]], Any]
) -> List[Dict[str, Any]]:
    """
    Добавляет новое вычисляемое поле ко всем записям в списке словарей.
    Args:
        data (List[Dict[str, Any]]): Исходный список словарей с данными.
        new_field (str): Имя нового поля.
        compute_func (Callable[[Dict[str, Any]], Any]):
            Функция, которая принимает один словарь (запись)
            в качестве аргумента и возвращает вычисляемое
            значение для нового поля.

    Returns:
        List[Dict[str, Any]]: Новый список словарей,
        где каждая запись содержит
        все исходные поля плюс новое вычисляемое поле.
    """
    res = []
    for record in data:
        new_rec = record.copy()
        new_rec[new_field] = compute_func(record)
        res.append(new_rec)
    return res
