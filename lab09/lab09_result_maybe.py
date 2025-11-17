# -*- coding: utf-8 -*-
"""
Лабораторна 9 — Помилки як дані: Maybe / Result (Either-патерн)

Цілі: відмова від винятків у домені; map/flat_map/chain.
Завдання: невдалий парсинг → Result; конвеєр перетворень з коротким замиканням на помилці.

Запуск:
    python lab09_result_maybe.py
Перевірка типів (опційно):
    mypy --config-file mypy_lab09.ini lab09_result_maybe.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any, Callable, Generic, Iterable, List, Tuple, TypeAlias, TypeVar, Union,
    TypedDict
)

# ===========================
# A) Базові типи: Maybe, Result
# ===========================

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")
F = TypeVar("F")

# -------- Maybe (Option) --------
@dataclass(frozen=True, slots=True)
class Some(Generic[T]):
    value: T

@dataclass(frozen=True, slots=True)
class Nothing:
    pass

Maybe: TypeAlias = Some[T] | Nothing  # параметризований тип-аліас


# -------- Result (Either) --------
@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T

@dataclass(frozen=True, slots=True)
class Err(Generic[E]):
    error: E

Result: TypeAlias = Ok[T] | Err[E]  # параметризований тип-аліас


# ===========================
# B) Комбінатори Result/Maybe
# ===========================

def map_result(r: Result[T, E], fn: Callable[[T], U]) -> Result[U, E]:
    """Якщо Ok — застосувати fn до value, інакше повернути Err як є."""
    if isinstance(r, Ok):
        return Ok(fn(r.value))
    return r  # type: ignore[return-value]  # Err[E] сумісний з Result[U, E]


def and_then(r: Result[T, E], fn: Callable[[T], Result[U, E]]) -> Result[U, E]:
    """flat_map: якщо Ok — викликати fn(value), якщо Err — коротке замикання."""
    if isinstance(r, Ok):
        return fn(r.value)
    return r  # type: ignore[return-value]


def map_err(r: Result[T, E], fn: Callable[[E], F]) -> Result[T, F]:
    """Перетворити тип помилки, не чіпаючи успіх."""
    if isinstance(r, Err):
        return Err(fn(r.error))
    return r  # type: ignore[return-value]


def unwrap_or(r: Result[T, E], default: T) -> T:
    """Дістати значення або повернути дефолт."""
    return r.value if isinstance(r, Ok) else default


# -- Maybe комбінатори --

def map_maybe(m: Maybe[T], fn: Callable[[T], U]) -> Maybe[U]:
    if isinstance(m, Some): return Some(fn(m.value))
    return m  # Nothing


def and_then_maybe(m: Maybe[T], fn: Callable[[T], Maybe[U]]) -> Maybe[U]:
    if isinstance(m, Some): return fn(m.value)
    return m  # Nothing


def to_result(m: Maybe[T], err: E) -> Result[T, E]:
    return Ok(m.value) if isinstance(m, Some) else Err(err)


# ===========================
# C) Обгортання викликів, що кидають
# ===========================

def try_call(fn: Callable[..., T], *args: Any, **kwargs: Any) -> Result[T, str]:
    """Виклик функції зі спійманим винятком → Result[T, str]."""
    try:
        return Ok(fn(*args, **kwargs))
    except Exception as e:  # вузькі винятки — ще краще, але для демо так
        return Err(str(e))


# ===========================
# D) Парсинг і конвеєр з коротким замиканням
# ===========================

def parse_int(s: str) -> Result[int, str]:
    s2 = s.strip()
    if s2 and (s2.isdigit() or (s2[0] in "+-" and s2[1:].isdigit())):
        return Ok(int(s2))
    return Err(f"Not an int: {s!r}")


def parse_pair(line: str) -> Result[tuple[str, int], str]:
    # Очікуємо "name,age"
    if "," not in line:
        return Err("Expected comma-separated 'name,age'")
    name, age_s = (part.strip() for part in line.split(",", 1))
    if not name:
        return Err("Empty name")
    return and_then(parse_int(age_s), lambda age: Ok((name.title(), age)))


class User(TypedDict):
    name: str
    age: int
    score: float


def validate_age(p: tuple[str, int]) -> Result[tuple[str, int], str]:
    name, age = p
    if 18 <= age <= 120:
        return Ok((name, age))
    return Err(f"Age out of range: {age}")


def calc_score(p: tuple[str, int]) -> Result[User, str]:
    name, age = p
    # Демонстраційна формула — замініть на доменну
    score = 10.0 - max(0, 25 - age) * 0.2
    return Ok(User(name=name, age=age, score=score))


def to_csv_row(u: User) -> Result[str, str]:
    return Ok(f'{u["name"]},{u["age"]},{u["score"]:.2f}')


def pipeline_line(line: str) -> Result[str, str]:
    """line -> parse_pair -> validate_age -> calc_score -> to_csv_row, з коротким замиканням."""
    r: Result[tuple[str, int], str] = parse_pair(line)
    r = and_then(r, validate_age)
    r2: Result[User, str] = and_then(r, calc_score)
    r3: Result[str, str] = and_then(r2, to_csv_row)
    return r3


# ===========================
# E) Обробка колекцій із зупинкою на першій помилці
# ===========================

def collect_results(items: Iterable[T], fn: Callable[[T], Result[U, E]]) -> Result[List[U], E]:
    acc: List[U] = []
    for it in items:
        r = fn(it)
        if isinstance(r, Err):
            return r
        acc.append(r.value)  # type: ignore[union-attr]
    return Ok(acc)


# Додатково: sequence/traverse (опційно, але корисно)
def sequence(rs: Iterable[Result[T, E]]) -> Result[List[T], E]:
    acc: List[T] = []
    for r in rs:
        if isinstance(r, Err):
            return r
        acc.append(r.value)  # type: ignore[union-attr]
    return Ok(acc)


def traverse(xs: Iterable[T], fn: Callable[[T], Result[U, E]]) -> Result[List[U], E]:
    return sequence(fn(x) for x in xs)


# ===========================
# F) Міні-тести
# ===========================

def _run_tests() -> None:
    # parse_int
    assert isinstance(parse_int(" 42 "), Ok) and parse_int(" 42 ").value == 42
    assert isinstance(parse_int("x"), Err)

    # parse_pair
    p = parse_pair("alice, 19")
    assert isinstance(p, Ok) and p.value == ("Alice", 19)

    # pipeline_line (успіх)
    ok = pipeline_line("alice, 26")
    assert isinstance(ok, Ok) and ok.value.startswith("Alice,26,")

    # pipeline_line (помилка віку)
    bad = pipeline_line("bob, 9")
    assert isinstance(bad, Err) and "Age out of range" in bad.error

    # collect_results зупиняється на першій помилці
    lines = ["alice, 26", "bad line", "carol, 21"]
    res = collect_results(lines, pipeline_line)
    assert isinstance(res, Err)

    # Maybe → Result
    m1: Maybe[int] = Some(5)
    m2: Maybe[int] = Nothing()
    assert isinstance(to_result(m1, "nope"), Ok) and to_result(m1, "nope").value == 5
    assert isinstance(to_result(m2, "nope"), Err)

    # sequence/traverse
    lst_ok = sequence([Ok(1), Ok(2), Ok(3)])
    assert isinstance(lst_ok, Ok) and lst_ok.value == [1,2,3]
    lst_err = sequence([Ok(1), Err("X"), Ok(3)])
    assert isinstance(lst_err, Err)
    trav = traverse(["alice, 26", "carol, 21"], pipeline_line)
    assert isinstance(trav, Ok) and len(trav.value) == 2

    print("All tests are passed.")

if __name__ == "__main__":
    _run_tests()
    demo = collect_results(["alice, 26", "bob, 17", "bad line", "carol, 21"], pipeline_line)
    print("Demonstration:", demo)
