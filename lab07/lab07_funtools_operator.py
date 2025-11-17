"""
Лабораторна 7 — functools та operator

Цілі: partial, reduce, singledispatch, total_ordering, itemgetter/attrgetter/methodcaller.
Завдання: (A) конвеєри з partial/reduce; (B) поліморфний API через singledispatch; (C) порядок порівняння через @total_ordering.

Інструкція:
- Запускайте цей файл як скрипт, щоб виконати демо та тести.
"""

from __future__ import annotations

from functools import partial, reduce, singledispatch, total_ordering
from operator import itemgetter, attrgetter, methodcaller
from pathlib import Path
from typing import Any, Iterable, Callable, Dict, List
import io, json, csv

# --- Вихідні "сирі" дані для прикладів ---
RAW_ROWS = [
    {"name": " ALICE ", "age": "19", "score": "8.5"},
    {"name": "bob", "age": "17", "score": "9.1"},
    {"name": "Carol", "age": "21", "score": "7.0"},
    {"name": "denis", "age": "20", "score": "9.3"},
]

# Геттери/метод-коллери
get_name, get_age, get_score = itemgetter("name"), itemgetter("age"), itemgetter("score")
strip, lower, title = methodcaller("strip"), methodcaller("lower"), methodcaller("title")


# ===========================
# A) Конвеєр обробки
# ===========================

def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Проганяє value через послідовність функцій."""
    return reduce(lambda acc, f: f(acc), funcs, value)


def mapf(fn: Callable[[Any], Any]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """Повертає функцію, що застосує map(fn, iterable)."""
    return partial(map, fn)


def filt(pred: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """Повертає функцію, що застосує filter(pred, iterable)."""
    return partial(filter, pred)


def normalize_row(r: Dict[str, Any]) -> Dict[str, Any]:
    """Повертає нормалізований словник з полями name:str, age:int, score:float."""
    return {
        "name": title(strip(get_name(r))),
        "age": int(get_age(r)),
        "score": float(get_score(r)),
    }


def build_clean_pipeline(rows: Iterable[Dict[str, Any]], top: int = 2) -> List[Dict[str, Any]]:
    """Сирі записи → нормалізація → фільтр повнолітніх → сортування → top-N."""
    adults = lambda r: r["age"] >= 18
    as_list = list
    # Сортування: score (спадання), name (зростання)
    sort_key = itemgetter("score", "name")

    def top_n(n: int) -> Callable[[Iterable[Any]], List[Any]]:
        def _take(it: Iterable[Any]) -> List[Any]:
            return list(it)[:n]
        return _take

    return pipeline(
        rows,
        mapf(normalize_row),
        filt(adults),
        as_list,
        partial(sorted, key=sort_key, reverse=True),
        top_n(top),
    )


# ===========================
# B) Поліморфний API (singledispatch)
# ===========================

@singledispatch
def load_users(src) -> List[Dict[str, Any]]:
    """Завантажити користувачів у форматі list[dict] з різних типів джерела."""
    raise TypeError(f"Unsupported type: {type(src)!r}")


@load_users.register
def _(src: str) -> List[Dict[str, Any]]:
    """Приймає JSON-рядок або шлях (до .json/.csv)."""
    s = src.strip()
    if s.startswith('[') or s.startswith('{'):
        data = json.loads(s)
        if isinstance(data, dict):
            data = [data]
        return data
    # Інакше вважаємо, що це шлях
    return load_users(Path(s))


@load_users.register
def _(src: Path) -> List[Dict[str, Any]]:
    """Читає .json (json.loads) та .csv (csv.DictReader)."""
    suf = src.suffix.lower()
    if suf == ".json":
        txt = src.read_text(encoding="utf-8")
        data = json.loads(txt)
        if isinstance(data, dict):
            data = [data]
        return data
    elif suf == ".csv":
        rows: List[Dict[str, Any]] = []
        with src.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows
    else:
        raise ValueError(f"Unsupported file type: {suf}")


@load_users.register
def _(src: io.TextIOBase) -> List[Dict[str, Any]]:
    """Відкритий файл: JSON через json.load, CSV через DictReader (за розширенням name)."""
    name = getattr(src, "name", "") or ""
    if str(name).lower().endswith(".csv"):
        rows: List[Dict[str, Any]] = []
        reader = csv.DictReader(src)
        for row in reader:
            rows.append(dict(row))
        return rows
    else:
        data = json.load(src)
        if isinstance(data, dict):
            data = [data]
        return data


@load_users.register
def _(src: list) -> List[Dict[str, Any]]:
    """Уже-готовий список словників (мінімальна валідація)."""
    if src and not isinstance(src[0], dict):
        raise ValueError("Expected list of dicts with user records")
    return src


# ===========================
# C) Порядок порівняння (@total_ordering)
# ===========================

@total_ordering
class Box:
    """Порядок: (volume, front_area, w)."""
    def __init__(self, w: float, h: float, d: float):
        self.w, self.h, self.d = float(w), float(h), float(d)

    def __repr__(self) -> str:
        return f"Box(w={self.w}, h={self.h}, d={self.d})"

    @property
    def volume(self) -> float:
        return self.w * self.h * self.d

    @property
    def front_area(self) -> float:
        return self.w * self.h

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Box):
            return NotImplemented
        # Порівнюємо за (об'єм, площа фронтальної грані, ширина)
        return (self.volume, self.front_area, self.w) == (other.volume, other.front_area, other.w)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Box):
            return NotImplemented
        # Порівнюємо за (об'єм, площа фронтальної грані, ширина)
        return (self.volume, self.front_area, self.w) < (other.volume, other.front_area, other.w)


# ===========================
# D) Тести
# ===========================

def _assert_eq(a, b, msg: str = ""):
    if a != b:
        raise AssertionError(f"Assertion failed: {a!r} != {b!r}. {msg}")


def test_pipeline_block():
    res = build_clean_pipeline(RAW_ROWS, top=3)
    names = [r["name"] for r in res]
    _assert_eq(names, ["Denis", "Alice", "Carol"])


def test_singledispatch_block(tmp_dir: Path = Path("./tmp_lab07")):
    # Створення тимчасової директорії для тестів
    tmp_dir.mkdir(exist_ok=True)

    json_str = '[{"name":"Alice","age":19},{"name":"Bob","age":17}]'
    lst = load_users(json_str)
    _assert_eq(isinstance(lst, list), True)
    _assert_eq(lst[0]["name"], "Alice")

    # JSON-файл
    p_json = tmp_dir / "users_test.json"
    p_json.write_text(json_str, encoding="utf-8")
    _assert_eq(load_users(p_json), lst)

    # CSV-файл
    p_csv = tmp_dir / "users_test.csv"
    p_csv.write_text("name,age\nCarol,21\nDenis,20\n", encoding="utf-8")
    rows = load_users(p_csv)
    _assert_eq(rows[0]["name"], "Carol")
    _assert_eq(rows[1]["age"], "20")

    # відкритий файл (JSON)
    with p_json.open(encoding="utf-8") as f:
        data2 = load_users(f)
        _assert_eq(data2, lst)

    # відкритий файл (CSV)
    with p_csv.open(encoding="utf-8") as f:
        data3 = load_users(f)
        _assert_eq(data3[0]["name"], "Carol")

    # список словників
    _assert_eq(load_users([{"name": "X"}])[0]["name"], "X")


def test_total_ordering_block():
    a = Box(1,2,3)  # V=6,  A=2, w=1
    b = Box(1,3,3)  # V=9,  A=3, w=1
    c = Box(1,2,6)  # V=12, A=2, w=1

    _assert_eq(a < b, True)
    _assert_eq(b < c, True)
    _assert_eq(max([a,b,c]), c)

    x = Box(2,2,3)  # V=12, A=4, w=2
    y = Box(3,1,4)  # V=12, A=3, w=3
    z = Box(2,2,3)  # рівний x

    ordered = sorted([c, x, y])
    _assert_eq(ordered[0], Box(1,2,6))
    _assert_eq(ordered[1], Box(3,1,4))
    _assert_eq(ordered[2], Box(2,2,3))
    _assert_eq(x == z, True)


def run_all_tests():
    tmp_dir = Path("./tmp_lab07")
    try:
        # Створення тимчасової директорії перед тестами
        tmp_dir.mkdir(exist_ok=True)
        test_pipeline_block()
        test_singledispatch_block(tmp_dir)
        test_total_ordering_block()
        print("All tests are passed!")
    except Exception as e:
        print(f"There is error while tests are running: {e}")
    finally:
        # Прибирання тимчасових файлів
        for f in tmp_dir.glob("*_test.*"):
            f.unlink()
        try:
             # Видалення папки, якщо вона порожня
            if any(tmp_dir.iterdir()) is False:
                tmp_dir.rmdir()
        except OSError:
            # Ігноруємо, якщо папка не порожня
            pass

if __name__ == "__main__":
    # Демонстрація конвеєра
    demo = build_clean_pipeline(RAW_ROWS, top=2)
    print("Conveyor demonstration (top=2):", demo)

    # Запуск тестів
    run_all_tests()