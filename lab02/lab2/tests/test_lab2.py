from __future__ import annotations

import copy
from typing import List

from lab2.lab2 import Record, build_pipeline, reduce_stats


def test_pipeline_top_and_sort() -> None:
    data: List[Record] = [
        {"id": 1, "name": "a", "age": 19, "city": "X", "purchases": [5, 5]},
        {"id": 2, "name": "b", "age": 19, "city": "Delhi", "purchases": [5, 6]},
        {"id": 3, "name": "c", "age": 17, "city": "Y", "purchases": [100]},
        {"id": 4, "name": "d", "age": 19, "city": "Delhi", "purchases": [1]},
    ]
    pipeline = build_pipeline(top_n=2, city="Delhi", factor=1.1)
    out = pipeline(data)
    # Adults only: ids 1,2,4. Totals: 10, 11*1.1=12.1, 1*1.1=1.1.
    # Sorted: 2,1 then 4 (but top 2 taken).
    assert [r["id"] for r in out] == [2, 1]
    assert out[0]["total"] == 12.1


def test_no_mutation() -> None:
    data: List[Record] = [
        {"id": 10, "name": " aa ", "age": 30, "city": "Delhi", "purchases": [1, 2, 3]},
    ]
    original = copy.deepcopy(data)
    pipeline = build_pipeline(top_n=1, city="Delhi", factor=2.0)
    _ = pipeline(data)
    assert data == original, "Input must not be mutated"


def test_reduce_stats() -> None:
    data: List[Record] = [
        {"id": 1, "name": "x", "age": 19, "city": "Delhi", "purchases": [10]},
        {"id": 2, "name": "y", "age": 19, "city": "Z", "purchases": [5]},
    ]
    out = build_pipeline(top_n=5, city="Delhi", factor=1.1)(data)
    stats = reduce_stats(out)
    # records: 2. totals: (10*1.1)=11, 5 -> sum=16, avg=8
    assert stats["count"] == 2.0
    assert abs(stats["sum_total"] - 16.0) < 1e-9
    assert abs(stats["avg_total"] - 8.0) < 1e-9
