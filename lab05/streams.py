from __future__ import annotations
from typing import Iterable, Iterator, TypeVar, Tuple, Callable
from collections import deque
from itertools import islice, count as _count, accumulate as _accumulate, takewhile as _takewhile, dropwhile as _dropwhile
import operator

T = TypeVar("T")

# --------- Нескінченні потоки ---------
def naturals(start: int = 0, step: int = 1) -> Iterator[int]:
    """Нескінченний потік цілих: start, start+step, ..."""
    # делегуємо в itertools.count заради ефективності
    yield from _count(start, step)

def fib_stream() -> Iterator[int]:
    """Нескінченний потік Фібоначчі: 0,1,1,2,3,5,..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# --------- Взяття / Пропуск ---------
def take(n: int, it: Iterable[T]) -> list[T]:
    """Повернути список із перших n елементів iterable. Якщо n <= 0 -> []."""
    if n <= 0:
        return []
    return list(islice(it, n))

def drop(n: int, it: Iterable[T]) -> Iterator[T]:
    """Повернути ітератор, що пропускає перші n елементів. Якщо n <= 0 -> повертає початковий."""
    if n <= 0:
        # пропускати нічого не треба
        yield from it
        return
    it = iter(it)
    # промотуємо n кроків
    next(islice(it, n, n), None)
    # повертаємо решту
    yield from it

# Умовні аналоги поверх itertools
def takewhile(pred: Callable[[T], bool], it: Iterable[T]) -> Iterator[T]:
    """Повертати елементи, поки предикат істинний."""
    yield from _takewhile(pred, it)

def dropwhile(pred: Callable[[T], bool], it: Iterable[T]) -> Iterator[T]:
    """Пропускати елементи, поки предикат істинний, далі віддавати все."""
    yield from _dropwhile(pred, it)

# --------- Обгортки для accumulate ---------
def accumulate_sum(it: Iterable[int]) -> Iterator[int]:
    """Префіксні суми (1,2,3) -> (1,3,6)."""
    yield from _accumulate(it)

def accumulate_prod(it: Iterable[int]) -> Iterator[int]:
    """Префіксні добутки (1,2,3) -> (1,2,6)."""
    yield from _accumulate(it, operator.mul)

def accumulate_custom(it: Iterable[T], func: Callable[[T, T], T]) -> Iterator[T]:
    """Загальна версія з довільною бінарною функцією."""
    yield from _accumulate(it, func)

# --------- Ковзні вікна ---------
def sliding_window(it: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Повертати послідовні вікна розміру k (кортежі) поверх iterable.
    Якщо k > len(it) для скінченної послідовності — нічого не віддаємо.
    Для нескінченних потоків вікна будуються ліниво.
    """
    if k <= 0:
        raise ValueError("k має бути додатним")
    it = iter(it)
    dq: deque[T] = deque(maxlen=k)

    # наповнюємо перше вікно
    for _ in range(k):
        try:
            dq.append(next(it))
        except StopIteration:
            return  # не вистачає елементів навіть на одне вікно

    # перше вікно
    yield tuple(dq)

    # наступні вікна
    for x in it:
        dq.append(x)  # deque автоматично витісняє найстаріше
        yield tuple(dq)

def moving_average(it: Iterable[float], k: int) -> Iterator[float]:
    """Лінива рухома середня з вікном k."""
    if k <= 0:
        raise ValueError("k має бути додатним")
    for win in sliding_window(it, k):
        yield sum(win) / k
