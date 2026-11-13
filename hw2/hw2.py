import csv
from collections import defaultdict


def read_file(file_name: str) -> list[dict]:
    """Считывает данные из CSV-файла и возвращает список словарей.
    Args:
        file_name (str): Путь к CSV-файлу.

    Returns:
        list[dict]: Список строк файла в виде словарей.
    """
    with open(file_name, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def hierarchy_dept(data: list[dict]) -> dict[str, set[str]]:
    """Группирует отделы по департаментам.

    Args:
        data (list[dict]): Список словарей с данными о сотрудниках.

    Returns:
        dict[str, set[str]]: Словарь, где ключ — название департамента,
        а значение — множество входящих в него отделов.
    """
    dept_info: dict[str, set[str]] = dict()
    for row in data:
        dept_info.setdefault(row["Департамент"], set()).add(row["Отдел"])
    return dept_info


def report_dept(data: list[dict]) -> dict[str, dict]:
    """Формирует сводный отчет по департаментам.
    Для каждого департамента считает численность сотрудников,
    минимальную, максимальную и среднюю заработную плату.

    Args:
        data (list[dict]): Список словарей с данными о сотрудниках.

    Returns:
        dict[str, dict]: Словарь с отчетами. Ключ — департамент,
        значение — словарь с метриками (численность, вилка, средняя).
    """
    dept_info: dict[str, dict] = defaultdict(
        lambda: {
            "Численность": 0,
            "Максимальная зарплата": float("-inf"),
            "Минимальная зарплата": float("inf"),
            "Сумма": 0,
        }
    )
    for row in data:
        info = dept_info[row["Департамент"]]
        salary = float(row["Оклад"])
        info["Численность"] += 1
        info["Максимальная зарплата"] = max(
            info["Максимальная зарплата"], salary
        )
        info["Минимальная зарплата"] = min(
            info["Минимальная зарплата"], salary
        )
        info["Сумма"] += salary
    for info in dept_info.values():
        info["Средняя зарплата"] = round(
            info["Сумма"] / info["Численность"], 2
        )
        del info["Сумма"]
    return dict(dept_info)


def save_file(report: dict, filename: str) -> None:
    """Сохраняет сводный отчет в CSV-файл.
    Args:
        report (dict): Словарь с готовым отчетом.
        filename (str): Имя (или путь) файла для сохранения.

    Returns:
        None
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        headers = [
            "Департамент",
            "Численность",
            "Максимальная зарплата",
            "Минимальная зарплата",
            "Средняя зарплата",
        ]

        writer.writerow(headers)

        for dept_name, info in report.items():
            writer.writerow(
                [
                    dept_name,
                    info["Численность"],
                    info["Максимальная зарплата"],
                    info["Минимальная зарплата"],
                    info["Средняя зарплата"],
                ]
            )


def save_report_to_csv(
    data: list[dict], filename: str = "dept_report.csv"
) -> None:
    """Генерирует сводный отчет и сохраняет его в файл.

    Args:
        data (list[dict]): Список словарей с данными о сотрудниках.
        filename (str, optional): Имя файла для сохранения.
            По умолчанию "dept_report.csv".

    Returns:
        None
    """
    report = report_dept(data)
    save_file(report, filename)
    print(f"Отчет успешно сохранен в файл: {filename}")


def main(report_number: int) -> None:
    """Готовит и выводит отчёт по выбранному варианту.

    Args:
        report_number (int): Номер отчёта (1 — иерархия,
            2 — сводка по департаментам, 3 — сохранение сводки в CSV).

    Returns:
        None
    """
    try:
        data = read_file("Corp_Summary.csv")
    except FileNotFoundError:
        print("Ошибка: файл Corp_Summary.csv не найден.")
        return

    match report_number:
        case 1:
            res = hierarchy_dept(data)
            if res:
                for dept, teams in res.items():
                    print(f"{dept}: {', '.join(teams)}")
        case 2:
            report = report_dept(data)
            for dept, info in report.items():
                print(f"Департамент: {dept}")
                print(f"    Численность: {info['Численность']}")
                print(
                    f"    Вилка: {info['Минимальная зарплата']} - "
                    f"{info['Максимальная зарплата']}"
                )
                print(f"    Средняя зарплата: {info['Средняя зарплата']}")
        case 3:
            save_report_to_csv(data, "report.csv")
        case _:
            print("Неверный номер отчёта. Введите число от 1 до 3.")


if __name__ == "__main__":
    main(int(input("Укажите номер отчёта от 1 до 3: ")))
