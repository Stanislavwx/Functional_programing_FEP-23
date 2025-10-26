from __future__ import annotations

import random

from lab04.algorithms import quicksort


def test_quicksort_basic() -> None:
    assert quicksort([]) == []
    assert quicksort([1]) == [1]
    assert quicksort([3, 2, 1]) == [1, 2, 3]
    assert quicksort([2, 2, 1, 3, 2]) == [1, 2, 2, 2, 3]


def test_quicksort_random() -> None:
    xs = [random.randint(-1000, 1000) for _ in range(1000)]
    assert quicksort(xs) == sorted(xs)
