from collections import Counter
from collections import defaultdict
from typing import TypedDict


class Order(TypedDict):
    id: int
    buyer: str
    status: str
    amount: int


class Day(TypedDict):
    day: str
    orders: int
    revenue: int
    returns: int


class Review(TypedDict):
    id: int
    product: str
    stars: int


def task1() -> None:
    moscow = {201, 202, 203, 204}
    kazan = {203, 204, 205, 206}

    print(f'Товары в любом из двух городов {moscow & kazan}')
    print(f'Только в Москве: {moscow - kazan}')
    print(f'Только в Казани: {kazan - moscow}')
    print(f'Уникальные товары на обоих складах вместе: {moscow | kazan}')


def task2() -> None:
    queries = [
        "чехол",
        "iphone",
        "чехол",
        "наушники",
        "iphone",
        "iphone",
        "кабель",
        "чехол",
        "iphone",
    ]

    count_values = Counter(queries)
    dict_count_values = dict(count_values)
    most_common = max(count_values, key=lambda q: count_values[q])

    print(f'Всего запросов в ленте: {len(queries)}')
    print(f'Сколько раз ввели каждый запрос: {dict_count_values}')
    print(f'Самый частый запрос: {most_common}')
    print(f'Доля: {dict_count_values[most_common] / len(queries):.2f}')

    count_values_one = {k: v for k, v in dict_count_values.items() if v == 1}
    print(f'Встретились один раз: {count_values_one}')


def task3() -> None:
    orders: list[Order] = [
        {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
        {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
        {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
        {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
        {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
        {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
    ]

    returned = [x for x in orders if x["status"] == "returned"]
    delivered = [x for x in orders if x["status"] == "delivered"]

    total_returned = sum(x["amount"] for x in returned)
    avg_delivered = sum(x["amount"] for x in delivered) / len(delivered)

    print(f'Сумма возвратов: {total_returned}')
    print(f'Вернули заказ: {[x["buyer"] for x in returned]}')
    print(f'Количество доставленных заказов: {len(delivered)}')
    print(f'Средний чек доставленных заказов: {avg_delivered}')


def task4() -> None:
    days: list[Day] = [
        {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
        {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
        {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
        {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
        {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
    ]

    total_revenue = sum(x["revenue"] for x in days)
    best_day = max(days, key=lambda d: d["revenue"])["day"]
    avg_revenue = {x["day"]: x["revenue"] / x["orders"] for x in days}
    bad_days = [x["day"] for x in days if x["returns"] > x["orders"] * 0.2]

    print(f'Выручка за неделю: {total_revenue}')
    print(f'День с самой большой выручкой: {best_day}')
    print(f'Средняя выручка на один заказ в каждый день: {avg_revenue}')
    print(f'Дни, где возвратов больше 20% заказов: {bad_days}')


def task5() -> None:
    reviews: list[Review] = [
        {"id": 1, "product": "Чехол", "stars": 5},
        {"id": 1, "product": "Чехол", "stars": 3},
        {"id": 1, "product": "Чехол", "stars": 4},
        {"id": 2, "product": "Наушники", "stars": 2},
        {"id": 2, "product": "наушники", "stars": 2},
        {"id": 2, "product": "НАУШНИКИ", "stars": 5},
        {"id": 3, "product": "Планшет", "stars": 5},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 4, "product": "Колонка", "stars": 4},
        {"id": 5, "product": "Кабель", "stars": 1},
    ]

    ratings = defaultdict(list)
    names = {}

    for r in reviews:
        pid = r["id"]
        ratings[pid].append(r["stars"])
        names[pid] = r["product"].lower()

    avg_products = {names[pid]: sum(s) / len(s) for pid, s in ratings.items()}
    print(f'Средняя оценка каждого товара: {avg_products}')

    avg_more_two = {pid: sum(s) / len(s) for pid, s in ratings.items()
                    if len(s) >= 2}
    worst_id = min(avg_more_two, key=lambda pid: avg_more_two[pid])
    print(f"Худший товар: {names[worst_id]} — {avg_more_two[worst_id]}")

    count_less = len([x for x in reviews if x["stars"] <= 2])
    print(f'Количество отзывов на 1 или 2 звезды: {count_less}')
    print(f'Доля 1 или 2х звёздочных отзывов среди всех:'
          f' {count_less / len(reviews)}')


def main() -> None:
    task1()
    task2()
    task3()
    task4()
    task5()


if __name__ == '__main__':
    main()
