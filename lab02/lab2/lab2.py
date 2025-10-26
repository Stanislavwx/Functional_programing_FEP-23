from __future__ import annotations

from functools import reduce
from itertools import islice
from typing import Any, Callable, Dict, Iterable, Iterator, List, Protocol, TypedDict

# ---- Types ----


class Record(TypedDict, total=False):
    id: int
    name: str
    age: int
    city: str
    purchases: List[float]
    total: float


Unary = Callable[[Any], Any]


class _UnaryProtocol(Protocol):
    def __call__(self, __x: Any, /) -> Any: ...


# ---- Functional helpers ----


def compose(*funcs: Unary) -> Unary:
    """Right-to-left function composition: compose(f, g)(x) == f(g(x))."""

    def _c(x: Any) -> Any:
        for f in reversed(funcs):
            x = f(x)
        return x

    return _c


def pipe(x: Any, *funcs: Unary) -> Any:
    """Left-to-right piping: pipe(x, f, g) == g(f(x))."""
    for f in funcs:
        x = f(x)
    return x


def juxt(*funcs: Unary) -> Callable[[Any], List[Any]]:
    """Apply many functions to the same input, collect results."""

    def _j(x: Any) -> List[Any]:
        return [f(x) for f in funcs]

    return _j


# ---- Pure transformations for the pipeline ----


def normalize_names() -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            yield {**r, "name": str(r.get("name", "")).strip().title()}

    return _f


def only_adults(min_age: int = 18) -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            if int(r.get("age", 0)) >= min_age:
                yield r

    return _f


def with_total() -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            purchases = r.get("purchases", []) or []
            yield {**r, "total": float(sum(purchases))}

    return _f


def boost_city(city: str, factor: float) -> Callable[[Iterable[Record]], Iterator[Record]]:
    def _f(recs: Iterable[Record]) -> Iterator[Record]:
        for r in recs:
            base = float(r.get("total", 0.0))
            boosted = base * factor if r.get("city") == city else base
            yield {**r, "total": round(boosted, 10)}  # stabilize floats

    return _f


def sort_by_total_desc() -> Callable[[Iterable[Record]], List[Record]]:
    def _f(recs: Iterable[Record]) -> List[Record]:
        return sorted(recs, key=lambda r: (-float(r.get("total", 0.0)), int(r.get("id", 0))))

    return _f


def take(n: int) -> Callable[[Iterable[Record]], List[Record]]:
    def _f(recs: Iterable[Record]) -> List[Record]:
        return list(islice(recs, n))

    return _f


# ---- Reductions / aggregations ----


def reduce_stats(recs: Iterable[Record]) -> Dict[str, float]:
    """Return count, sum_total, avg_total without mutating inputs."""
    init: Dict[str, float] = {"count": 0.0, "sum_total": 0.0}
    acc = reduce(
        lambda a, r: {
            "count": a["count"] + 1.0,
            "sum_total": a["sum_total"] + float(r.get("total", 0.0)),
        },
        recs,
        init,
    )
    avg = acc["sum_total"] / acc["count"] if acc["count"] else 0.0
    return {"count": acc["count"], "sum_total": acc["sum_total"], "avg_total": avg}


# ---- Build pipeline ----


def build_pipeline(
    top_n: int = 2,
    city: str = "Delhi",
    factor: float = 1.1,
) -> Callable[[Iterable[Record]], List[Record]]:
    """Return a composite function that transforms a stream of records."""
    return compose(
        take(top_n),
        sort_by_total_desc(),
        boost_city(city, factor),
        with_total(),
        only_adults(18),
        normalize_names(),
    )
