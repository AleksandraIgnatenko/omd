from typing import List, Dict, Any, Callable
from json_dict_processing import (
    extract_nested_value,
    process_dictionary_with_config,
    process_list_of_dicts_with_config,
    create_processor,
)
from aggregations import (
    calc_mean, calc_median, calc_max, calc_min, calc_count, calc_sum, get_top_n
)
from dataset_helpers import (
    filter_data, group_by_attributes, apply_aggregation, get_all_unique_fields
)
from attribute_manager import add_computed_field
from laureates_helpers import (
    adjust_country_for_migration, analyze_migration, extract_refused_prizes,
    get_award_country_from_raw, HISTORICAL_COUNTRY_MAPPING,
)


def test_json_dict_processing() -> None:
    """
    Проверяет корректность извлечения вложенных значений
    и обработки словарей по конфигу.

    Покрывает:
        extract_nested_value: вложенные пути, отсутствующие ключи,
        None на промежуточных уровнях.
        process_dictionary_with_config: три типа правил.
        process_list_of_dicts_with_config: обработка списка, пустой список.
        create_processor: фабрика возвращает рабочие процессоры обоих типов.
    """

    sample: Dict[str, Any] = {
        'id': '42',
        'knownName': {'en': 'Test Laureate', 'se': 'Test Laureate'},
        'birth': {
            'date': '1901-12-05',
            'place': {
                'country': {'en': 'Prussia'},
                'countryNow': {'en': 'Germany'}
            },
        },
        'nobelPrizes': [
            {'awardYear': '1935', 'category': {'en': 'Physics'}},
            {'awardYear': '1950', 'category': {'en': 'Chemistry'}},
        ],
    }

    # extract_nested_value
    assert extract_nested_value(sample, ['knownName', 'en']) == 'Test Laureate'
    assert extract_nested_value(
        sample,
        ['birth', 'place', 'country', 'en']
    ) == 'Prussia'
    assert extract_nested_value(sample, ['no', 'such', 'key']) is None
    assert extract_nested_value(None, ['any']) is None

    # process_dictionary_with_config
    config: Dict[str, Any] = {
        'name': ['knownName', 'en'],
        'country': ['birth', 'place', 'country', 'en'],
        'id_int': (['id'], int),
        'missing': ['no', 'such', 'key'],
    }
    result = process_dictionary_with_config(sample, config)
    assert result['name'] == 'Test Laureate'
    assert result['country'] == 'Prussia'
    assert result['id_int'] == 42 and isinstance(result['id_int'], int)
    assert result['missing'] is None

    assert sample['id'] == '42' and isinstance(sample['id'], str)

    # process_list_of_dicts_with_config
    list_result = process_list_of_dicts_with_config([sample, sample], config)
    assert len(list_result) == 2
    assert process_list_of_dicts_with_config([], config) == []

    # create_processor
    single_proc = create_processor(config, list_processor=False)
    list_proc = create_processor(config, list_processor=True)
    assert single_proc(sample) == result
    assert list_proc([sample]) == [result]


def test_aggregations() -> None:
    """
    Проверяет статистические функции и get_top_n.
    """
    # Базовые случаи
    assert calc_mean([1, 2, 3, 4]) == 2.5
    assert calc_median([1, 2, 3, 4]) == 2.5
    assert calc_median([3, 1, 2]) == 2
    assert calc_min([5, 1, 3]) == 1
    assert calc_max([5, 1, 3]) == 5
    assert calc_sum([1, 2, 3]) == 6
    assert calc_count([1, 2, 3]) == 3

    # Пустой список
    assert calc_mean([]) is None
    assert calc_median([]) is None
    assert calc_min([]) is None
    assert calc_max([]) is None
    assert calc_sum([]) == 0
    assert calc_count([]) == 0

    # get_top_n
    data: List[Dict[str, Any]] = [
        {'name': 'a', 'v': 10},
        {'name': 'b', 'v': 30},
        {'name': 'c', 'v': 20},
        {'name': 'd', 'v': None},
    ]
    assert [d['name'] for d in get_top_n(data, 'v', 2)] == ['b', 'c']
    assert [d['name'] for d in get_top_n(
        data,
        'v',
        2,
        reverse=False)
    ] == ['a', 'c']
    assert len(get_top_n(data, 'v', 100)) == 3
    assert get_top_n(data, 'absent_key', 5) == []


def test_dataset_helpers() -> None:
    """
    Проверяет функции работы с наборами данных.
    """
    toy: List[Dict[str, Any]] = [
        {'cat': 'A', 'v': 1},
        {'cat': 'A', 'v': 3},
        {'cat': 'B', 'v': None},
    ]

    # filter_data
    assert len(filter_data(toy, lambda r: r['cat'] == 'A')) == 2
    assert filter_data([], lambda r: True) == []

    # group_by_attributes
    grouped = group_by_attributes(toy, ['cat'])
    assert set(grouped.keys()) == {('A',), ('B',)}
    assert len(grouped[('A',)]) == 2

    # apply_aggregation
    assert apply_aggregation(toy, 'v', calc_mean) == 2.0
    assert apply_aggregation(grouped[('B',)], 'v', calc_mean) is None

    # get_all_unique_fields
    fields = get_all_unique_fields([{'a': 1, 'b': 2}, {'b': 3, 'c': 4}])
    assert fields == ['a', 'b', 'c']


def test_attribute_manager() -> None:
    """
    Проверяет add_computed_field
    """
    toy: List[Dict[str, Any]] = [{'v': 1}, {'v': 2}]
    enriched = add_computed_field(toy, 'v_double', lambda r: r['v'] * 2)

    assert enriched[0]['v_double'] == 2
    assert enriched[1]['v_double'] == 4
    assert 'v_double' not in toy[0]
    assert len(enriched) == len(toy)


def test_laureates_helpers() -> None:
    """
    Проверяет функции для анализа лауреатов.
    """
    # Маппинг стран
    assert adjust_country_for_migration('Prussia') == 'Germany'
    assert adjust_country_for_migration('West Germany') == 'Germany'
    assert adjust_country_for_migration('USSR') == 'Russia'
    assert adjust_country_for_migration('USA') == 'USA'
    assert adjust_country_for_migration(None) is None

    for historical, modern in HISTORICAL_COUNTRY_MAPPING.items():
        assert adjust_country_for_migration(modern) == modern

    # analyze_migration
    person_migrant = {
        'country_birth': 'Prussia',
        'award_country': 'USA',
    }
    mig = analyze_migration(person_migrant)
    assert mig['is_migrant'] is True
    assert mig['country_of_origin_adjusted_for_migration'] == 'Germany'
    assert mig['country_now'] == 'USA'

    person_non_migrant = {
        'country_birth': 'USA',
        'award_country': 'USA',
    }
    assert analyze_migration(person_non_migrant)['is_migrant'] is False

    # extract_refused_prizes
    refuse_toy: Dict[str, Any] = {
        'prizes_relevant': [
            {'prize_status': 'received'},
            {'prize_status': 'declined'},
            {'prize_status': 'restricted'},
        ]
    }
    assert len(extract_refused_prizes(refuse_toy)) == 2
    assert extract_refused_prizes({'prizes_relevant': []}) == []
    assert extract_refused_prizes({}) == []

    # get_award_country_from_raw
    assert get_award_country_from_raw({
        'nobelPrizes': [
            {
                'awardYear': '1921',
                'affiliations': [{'country': {'en': 'Germany'}}]
            }
        ]
    }) == 'Germany'

    assert get_award_country_from_raw({
        'nobelPrizes': [
            {
                'awardYear': '1950',
                'affiliations': [{'country': {'en': 'USA'}}]
            },
            {
                'awardYear': '1935',
                'affiliations': [{'country': {'en': 'UK'}}]
            },
        ]
    }) == 'UK'

    assert get_award_country_from_raw({'nobelPrizes': []}) is None

    assert get_award_country_from_raw({
        'nobelPrizes': [{'awardYear': '1921'}]
    }) is None

    assert get_award_country_from_raw({}) is None


def run_all_tests() -> None:
    """Запускает все тестовые функции и выводит итоговый отчёт."""
    tests: List[Callable[[], None]] = [
        test_json_dict_processing,
        test_aggregations,
        test_dataset_helpers,
        test_attribute_manager,
        test_laureates_helpers,
    ]

    failed: List[str] = []
    for test_fn in tests:
        try:
            test_fn()
            print(f'{test_fn.__name__}')
        except AssertionError as e:
            failed.append(test_fn.__name__)
            print(f'{test_fn.__name__}: {e}')

    print()
    if failed:
        print(f"Провалено тестов: {len(failed)} — {failed}")
    else:
        print(f"Все {len(tests)} тестов пройдены успешно")


if __name__ == '__main__':
    run_all_tests()
