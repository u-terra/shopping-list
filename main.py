"""«Список покупок» — простая консольная программа.

Что умеет:
  * добавлять товары;
  * показывать список;
  * удалять товары по номеру.

Список сохраняется в файл shopping_list.json рядом с программой,
поэтому после перезапуска товары остаются на месте.
Используется только стандартная библиотека Python.
"""

import json
from pathlib import Path

# Файл, в котором хранится список. Лежит в той же папке, что и main.py.
DATA_FILE = Path(__file__).with_name("shopping_list.json")

MENU = """
===== СПИСОК ПОКУПОК =====
  1. Добавить товар
  2. Показать список
  3. Удалить товар
  0. Выход
"""


def load_items() -> list[str]:
    """Читает товары из файла. Если файла нет — возвращает пустой список."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        print("Не удалось прочитать сохранённый список — начинаем с пустого.")
        return []
    # На всякий случай проверяем, что в файле действительно список строк.
    return [str(item) for item in data] if isinstance(data, list) else []


def save_items(items: list[str]) -> None:
    """Записывает текущий список в файл."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def add_item(items: list[str], name: str) -> None:
    """Добавляет товар в список."""
    name = name.strip()
    if not name:
        print("Название не может быть пустым.")
        return
    items.append(name)
    save_items(items)
    print(f"Добавлено: {name}")


def show_items(items: list[str]) -> None:
    """Печатает список с номерами."""
    if not items:
        print("Список пуст. Добавьте что-нибудь!")
        return
    print("\nВаш список:")
    for number, item in enumerate(items, start=1):
        print(f"  {number}. {item}")


def remove_item(items: list[str], number: int) -> None:
    """Удаляет товар по его номеру в списке."""
    if not 1 <= number <= len(items):
        print("Товара с таким номером нет.")
        return
    removed = items.pop(number - 1)
    save_items(items)
    print(f"Удалено: {removed}")


def ask_number(prompt: str) -> int | None:
    """Спрашивает у пользователя число. Возвращает None, если введено не число."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Нужно ввести число.")
        return None


def main() -> None:
    items = load_items()
    print("Добро пожаловать в «Список покупок»!")

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_item(items, input("Что добавить: "))
        elif choice == "2":
            show_items(items)
        elif choice == "3":
            show_items(items)
            if items:
                number = ask_number("Номер товара для удаления: ")
                if number is not None:
                    remove_item(items, number)
        elif choice == "0":
            print(f"Пока! Список сохранён в файле {DATA_FILE.name}.")
            break
        else:
            print("Такого пункта нет. Введите 0, 1, 2 или 3.")


if __name__ == "__main__":
    main()
