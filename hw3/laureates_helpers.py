import re
from typing import Dict, Any, Tuple, Optional, List


def get_first_prize_info(
    record: Dict[str, Any]
) -> Tuple[Optional[int], Optional[str]]:
    """
    Возвращает год и категорию самого раннего приза лауреата.

    Args:
        record: словарь с данными лауреата

    Returns:
        Кортеж (год_первого_приза, категория).
        Если призов нет или у них нет года — возвращает (None, None).
    """
    prizes = record.get('prizes_relevant', [])
    valid_prizes = [p for p in prizes if p.get('award_year') is not None]
    if not valid_prizes:
        return None, None

    first_prize = min(valid_prizes, key=lambda x: x['award_year'])
    return first_prize.get('award_year'), first_prize.get(
        'category_en', 'Unknown'
    )


HISTORICAL_COUNTRY_MAPPING: Dict[str, str] = {
    'USSR': 'Russia',
    'Russian Empire': 'Russia',
    'Prussia': 'Germany',
    'West Germany': 'Germany',
    'East Germany': 'Germany',
    'Bavaria': 'Germany',
    'Württemberg': 'Germany',
    'Mecklenburg': 'Germany',
    'East Friesland': 'Germany',
    'Hesse-Kassel': 'Germany',
    'Schleswig': 'Germany',
    'Austrian Empire': 'Austria',
    'Austria-Hungary': 'Austria',
    'Tuscany': 'Italy',
    'Crete': 'Greece',
    'German-occupied Poland': 'Poland',
    'Free City of Danzig': 'Poland',
    'Belgian Congo': 'Democratic Republic of the Congo',
    'French Algeria': 'Algeria',
    'French protectorate of Tunisia': 'Tunisia',
    'British Mandate of Palestine': 'Israel',
    'British Protectorate of Palestine': 'Israel',
    'British India': 'India',
    'Gold Coast': 'Ghana',
    'Southern Rhodesia': 'Zimbabwe',
    'Java, Dutch East Indies': 'Indonesia',
    'Burma': 'Myanmar',
    'Persia': 'Iran',
    'Ottoman Empire': 'Turkey',
    'Czechoslovakia': 'Czech Republic',
    'Korea': 'South Korea',
    'Tibet': 'China',
    'Guadeloupe, France': 'France',
    'Faroe Islands (Denmark)': 'Denmark',
    'British West Indies': 'Jamaica',
    'Northern Ireland': 'United Kingdom',
}


def adjust_country_for_migration(country: Optional[str]) -> Optional[str]:
    """
    Корректирует историческое название страны на современное
    для корректного анализа миграции.

    Args:
        country: Исходное название страны (может быть None).

    Returns:
        Современное название страны или исходное, если маппинг не найден.
    """
    if country is None:
        return None
    return HISTORICAL_COUNTRY_MAPPING.get(country, country)


def analyze_migration(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Определяет, является ли лауреат мигрантом, сравнивая страну рождения
    (с учетом исторических изменений) и страну на момент награждения.

    Args:
        record: Словарь с данными лауреата.

    Returns:
        Словарь с полями:
            'is_migrant' (bool): Факт миграции.
            'country_of_origin_adjusted_for_migration' (Optional[str]):
                Скорректированная страна происхождения.
            'country_now' (Optional[str]): Страна на момент награждения.
    """
    origin: Optional[str] = record.get('country_birth')
    destination: Optional[str] = record.get('award_country')

    adjusted_origin: Optional[str] = adjust_country_for_migration(origin)
    adjusted_destination: Optional[str] = adjust_country_for_migration(
        destination
    )

    is_migrant: bool = bool(
        adjusted_origin and
        adjusted_destination and
        adjusted_origin != adjusted_destination
    )

    return {
        'is_migrant': is_migrant,
        'country_of_origin_adjusted_for_migration': adjusted_origin,
        'country_now': adjusted_destination
    }


def calc_migration_stats(
    data: List[Dict[str, Any]],
    country_field: str
) -> List[Dict[str, Any]]:
    """
    Считает долю мигрантов для каждой страны без фильтрации по количеству.

    Args:
        data: Список словарей с данными лауреатов.
            Каждый словарь должен содержать:
                'is_migrant' (bool): Факт миграции
                country_field (str): Название страны
        country_field: Имя поля, по которому группируем.

    Returns:
        Список словарей со статистикой по каждой стране, содержащий:
            'country' (str): Название страны
            'total' (int): Общее количество лауреатов из этой страны
            'migrants' (int): Количество лауреатов-мигрантов
            'percentage' (float): Доля мигрантов в процентах
    """
    groups: Dict[str, Dict[str, int]] = {}

    for record in data:
        country: Optional[str] = record.get(country_field)
        if country is None:
            continue

        if country not in groups:
            groups[country] = {'total': 0, 'migrants': 0}

        groups[country]['total'] += 1
        if record.get('is_migrant'):
            groups[country]['migrants'] += 1

    stats: List[Dict[str, Any]] = []
    for country, counts in groups.items():
        percentage: float = (counts['migrants'] / counts['total']) * 100
        stats.append({
            'country': country,
            'total': counts['total'],
            'migrants': counts['migrants'],
            'percentage': percentage
        })

    return stats


def extract_refused_prizes(record: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Извлекает список призов, от которых лауреат отказался.

    Args:
        record: Словарь с данными лауреата.

    Returns:
        Список словарей с данными об отказанных призах.
    """
    prizes: List[Dict[str, Any]] = record.get('prizes_relevant', [])
    return [p for p in prizes if p.get('prize_status') in (
        'declined', 'restricted'
    )]


def get_award_country_from_raw(raw_laureate: Dict[str, Any]) -> Optional[str]:
    """
    Извлекает страну на момент получения первой премии.
    Args:
        raw_laureate: Исходный словарь лауреата.

    Returns:
        Название страны на английском (str) или None.
    """
    prizes: List[Dict[str, Any]] = raw_laureate.get('nobelPrizes', [])
    if not prizes:
        return None

    valid_prizes = [p for p in prizes if p.get('awardYear')]
    if not valid_prizes:
        return None

    first_prize: Dict[str, Any] = min(
        valid_prizes,
        key=lambda x: x['awardYear']
    )

    affiliations: List[Dict[str, Any]] = first_prize.get('affiliations', [])
    if affiliations and isinstance(affiliations, list) and len(
        affiliations
    ) > 0:
        first_aff: Dict[str, Any] = affiliations[0]
        if isinstance(first_aff, dict):
            country_data: Any = first_aff.get('country')
            if isinstance(country_data, dict):
                return country_data.get('en')

    return None


def tokenize_text(text: str) -> List[str]:
    """
    Разбивает текст на слова (токены).
    Приводит к нижнему регистру,
    оставляет только последовательности латинских букв.

    Args:
        text: Исходный текст мотивации.

    Returns:
        Список слов в нижнем регистре.
    """
    if not text:
        return []
    return re.findall(r'\b[a-z]+\b', text.lower())
