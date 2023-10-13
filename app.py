import sys
import csv
from typing import Optional, Callable, List, Dict


def reader(path: str) -> List[List[str]]:
    """
    Reads all rows of the file except header
    """

    data = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        for row in reader:
            data.append(row)
    return data


def arg_checker(func: Callable):
    """
    Decorator to check if *args are correct or not
    """
    def wrapper(*args: Optional[str], **kwargs: Dict):
        dep_names = ["Разработка", "Маркетинг",
                     "Бухгалтерия", "Аналитика", "Продажи"]
        for arg in args:
            if arg.title() not in dep_names:
                raise ValueError("Такого Департамента не существует")
        func(*args, **kwargs)
    return wrapper


def get_department_teams(data: List[List[str]]) -> Dict[str, set[str]]:
    """
    Gets all teams grouped in corresponding department
    """
    department_teams = dict()

    for row in data:
        department_name = row[1]
        if department_name not in department_teams.keys():
            department_teams[department_name] = set()
        team_name = row[2]
        department_teams[department_name].add(team_name)
    return department_teams


def get_department_stats(data: List[List[str]]) -> Dict[str, list]:
    """
    Gest statistics of each department
    Stats include number of employees, min, max, mean salaries
    """
    dep_stats = dict()

    for row in data:
        department_name = row[1]
        salary = int(row[5])
        if department_name not in dep_stats.keys():
            dep_stats[department_name] = [0, float("inf"), 0, 0]
        dep_stats[department_name][0] += 1
        if salary < dep_stats[department_name][1]:
            dep_stats[department_name][1] = salary
        if salary > dep_stats[department_name][2]:
            dep_stats[department_name][2] = salary
        dep_stats[department_name][-1] += salary
    for name in dep_stats.keys():
        dep_stats[name][-1] /= dep_stats[name][0]
    return dep_stats


@arg_checker
def show_department_info(*args: Optional[str], dep_teams: Dict[str, set[str]]):
    """
    Shows all teams of the corresponding department
    """
    print()
    print("="*70)
    print(f"{'Департамент':<{13}}| Отделы")
    print("="*70)
    if args:
        for arg in args:
            teams = ', '.join(dep_teams[arg.title()])
            print(f"{arg.title():<{13}}| {teams}")
            print("-"*70)
    else:
        for name, teams in dep_teams.items():
            teams = ', '.join(dep_teams[name])
            print(f"{name:<{13}}| {teams}")
            print("-"*70)


@arg_checker
def show_department_stats(*args: Optional[str], dep_stats: Dict[str, List]):
    """
    Shows all statistics of the corresponding department
    """
    print()
    print("="*80)
    print(f"{'Департамент':<{13}}| {'Численность':<{13}}| "
          f"{'Мин. Зарплата':<{13}}| {'Макс. Зарплата':<{15}}|"
          f"{'Сред. Зарплата':<{13}}")
    print("="*80)
    if args:
        for arg in args:
            arg = arg.title()
            employee_num = dep_stats[arg][0]
            min_salary = dep_stats[arg][1]
            max_salary = dep_stats[arg][2]
            mean_salary = dep_stats[arg][3]
            print(f"{arg:<{13}}| {employee_num:<{13}}| "
                  f"{min_salary:<{13}}| {max_salary:<{15}}| "
                  f"{mean_salary:.4f}")
            print("-"*80)
    else:
        for name, stats in dep_stats.items():
            print(f"{name:<{13}}| {stats[0]:<{13}}| "
                  f"{stats[1]:<{13}}| {stats[2]:<{15}}| "
                  f"{stats[3]:.4f}")
            print("-"*80)


def save_stats(dep_stats: Dict[str, List]):
    """
    Saves all statistics of the corresponding departments in the
    csv file
    """
    path = "Report.csv"

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        header = ["Департамент", "Численность", "Мин. Зарплата",
                  "Макс. Зарплата", "Сред. Зарплата"]
        writer.writerow(header)
        for name, row in dep_stats.items():
            writer.writerow([name, *row])


def display_menu(data: List[List[str]]):
    """
    Menu display that contains available options
    """
    choice = ""
    options = [1, 2, 3, 4]

    while True:
        print("\n==========Меню==========")
        print("1. Информация о Департаментах")
        print("2. Сводный отчёт по Демартаментам")
        print("3. Сохранить сводный отчёт")
        print("4. Выход")
        print("========================")
        choice = input("\n>>Выбрать: ")
        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice not in options:
            continue

        teams = get_department_teams(data)
        stats = get_department_stats(data)
        if choice == 1:
            deps = input("\n>>Введите имена Департаментов через пробел"
                         "(нажмите <Enter> для всех департаментов):")
            if deps:
                show_department_info(*deps.split(), dep_teams=teams)
            else:
                show_department_info(dep_teams=teams)
        elif choice == 2:
            deps = input("\n>>Введите имена Департаментов через пробел"
                         "(нажмите <Enter> для всех департаментов):")
            if deps:
                show_department_stats(*deps.split(), dep_stats=stats)
            else:
                show_department_stats(dep_stats=stats)
        elif choice == 3:
            save_stats(dep_stats=stats)
        else:
            sys.exit()


def start_program():
    """
    Main function that starts program
    """
    file_path = "Corp_Summary.csv"
    data = reader(file_path)

    display_menu(data)


if __name__ == "__main__":
    start_program()
