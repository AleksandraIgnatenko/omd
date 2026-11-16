from typing import Callable, Any
from json_dict_processing import create_processor


CONFIG_PRIZE: dict[str, list[str] | tuple[list[str], Callable[[Any], Any]]] = {
    'prize_amount': ['prizeAmount'],
    'prize_amount_adjusted': ['prizeAmountAdjusted'],
    'award_year': (['awardYear'], int),
    'category_en': ['category', 'en'],
    'prize_status': ['prizeStatus'],
    'motivation_en': ['motivation', 'en']
}


def prize_processor(
) -> Callable[[list[dict[str, Any]]], list[dict[str, Any]]]:
    """Создаёт процессор для обработки списка призов.

    Returns:
        Callable[[list[dict[str, Any]]], list[dict[str, Any]]]:
        Функция-процессор, принимающая список исходных призов
        и возвращающая список обработанных призов.
    """
    return create_processor(CONFIG_PRIZE, list_processor=True)
