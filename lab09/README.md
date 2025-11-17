# Лабораторна робота №9 — Maybe / Result

Ця робота демонструє патерн «Помилки як дані» на прикладі типів `Maybe` та `Result` (Either). У файлі `lab09_result_maybe.py` реалізовано власні варіанти `Some/Nothing` і `Ok/Err`, а також набір комбінаторів (`map`, `and_then`, `map_err`, `unwrap_or`) для побудови декларативних конвеєрів без винятків.

## Структура проєкту
- `lab09_result_maybe.py` — основний модуль з реалізацією типів, комбінаторів, прикладом парсингу CSV-рядків та міні-тестами.
- `lab09_result_maybe.ipynb` — за потреби, блокнот із тими ж прикладами (не обов’язковий для запуску).

## Запуск
```bash
python lab09_result_maybe.py
```
Скрипт запускає `_run_tests()` (юнiт-тести на ключові функції) і виводить демонстраційний результат конвеєра `collect_results`.

## Перевірка типів (опційно)
```bash
mypy --config-file mypy_lab09.ini lab09_result_maybe.py
```
Файл `mypy_lab09.ini` повинен лежати поруч із лабораторною.

## Короткий опис завдання
1. Реалізувати типи `Maybe` та `Result` для безвиняткової обробки помилок.
2. Написати комбінатори `map`, `and_then`, `map_err`, `unwrap_or`, а також їх аналоги для `Maybe`.
3. Побудувати конвеєр обробки рядка `name, age` з функціями `parse_pair → validate_age → calc_score → to_csv_row`, який коротко замикається на першій помилці.
4. Реалізувати функцію `collect_results` (і опційно `sequence`/`traverse`) для зупинки на першому `Err` в ітерації.

## Демонстраційний сценарій
```
alice, 26     -> Ok('Alice,26,9.20')
bob, 17       -> Err('Age out of range: 17')
bad line      -> Err("Expected comma-separated 'name,age'")
carol, 21     -> Ok('Carol,21,6.80')
```
Функція `collect_results` обробляє список рядків та повертає `Ok[List[str]]` або перший `Err`.
