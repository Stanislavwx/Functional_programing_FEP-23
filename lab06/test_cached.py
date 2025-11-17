from __future__ import annotations

from typing import Any, cast
from decorators import cached


def test_cached_ttl_and_clear_and_invalidate() -> None:
    t = 1000.0
    def time_fn() -> float:
        return t

    hits = {"n": 0}

    @cached(ttl=1.0, time_fn=time_fn)
    def f(x: int, k: int = 1) -> int:
        hits["n"] += 1
        return x * k

    # перше обчислення
    assert f(10, k=2) == 20
    assert hits["n"] == 1

    # кешований хіт
    assert f(10, k=2) == 20
    assert hits["n"] == 1

    # TTL минув
    t += 2.0
    assert f(10, k=2) == 20
    assert hits["n"] == 2

    # інвалідація за предикатом
    removed = cast(Any, f).cache_invalidate(lambda args, kwargs: args == (10,) and kwargs.get("k") == 2)
    assert removed >= 1
    assert f(10, k=2) == 20
    assert hits["n"] == 3

    # повне очищення
    cast(Any, f).cache_clear()
    assert f(5) == 5
    assert hits["n"] == 4
