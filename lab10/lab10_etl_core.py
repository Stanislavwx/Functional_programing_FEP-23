# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Callable, TypedDict, TypeAlias, Any, List, Dict
from functools import reduce
from operator import methodcaller
import re

class Raw(TypedDict):
    name: str
    age: str
    country: str
    email: str

class Row(TypedDict):
    name: str
    age: int
    country: str
    email: str

class Out(TypedDict):
    name: str
    age: int
    email: str
    segment: str

@dataclass(frozen=True)
class Ok:
    value: Any

@dataclass(frozen=True)
class Err:
    error: str

Result: TypeAlias = Ok | Err

def map_result(r: Result, fn: Callable[[Any], Any]) -> Result:
    return Ok(fn(r.value)) if isinstance(r, Ok) else r

def and_then(r: Result, fn: Callable[[Any], Result]) -> Result:
    return fn(r.value) if isinstance(r, Ok) else r

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return lambda x: reduce(lambda acc, f: f(acc), reversed(funcs), x)

def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    return reduce(lambda acc, f: f(acc), funcs, value)

strip = methodcaller("strip")
lower = methodcaller("lower")
title = methodcaller("title")

def only_digits(s: str) -> str:
    s2 = strip(s)
    if not s2:
        return ""
    out = []
    for i, ch in enumerate(s2):
        if ch.isdigit() or (i == 0 and ch in "+-"):
            out.append(ch)
    return "".join(out)

def to_int(s: str) -> int:
    s2 = only_digits(s)
    if s2 in ("", "+", "-"):
        raise ValueError(f"Cannot convert to int: {s!r}")
    return int(s2)

def safe_to_int(s: str) -> Result:
    try:
        return Ok(to_int(s))
    except ValueError as e:
        return Err(str(e))

def to_cc(s: str) -> str:
    return strip(s).upper()[:2]

def norm_email(s: str) -> str:
    return lower(strip(s))

def norm_name(s: str) -> str:
    return title(strip(s))

def normalize(raw: Raw) -> Result:
    age_r = safe_to_int(raw["age"])
    
    if isinstance(age_r, Err):
        return Err(f"Parsing failed for name={raw['name']!r}: {age_r.error}")

    return Ok({
        "name":    norm_name(raw["name"]),
        "age":     age_r.value,
        "country": to_cc(raw["country"]),
        "email":   norm_email(raw["email"]),
    })

EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)
ALLOWED_CC = {"UA","IN","IT","GR","US","GB","DE","FR","ES"}

def validate_age(row: Row) -> Result:
    return Ok(row) if 0 <= row["age"] <= 120 else Err(f"Bad age: {row['age']}")

def validate_email(row: Row) -> Result:
    return Ok(row) if EMAIL_RE.match(row["email"]) else Err(f"Bad email: {row['email']}")

def validate_cc(row: Row) -> Result:
    return Ok(row) if row["country"] in ALLOWED_CC else Err(f"Bad country: {row['country']}")

def validate_all(r: Result) -> Result:
    r = and_then(r, validate_age)
    r = and_then(r, validate_email)
    r = and_then(r, validate_cc)
    return r

def segment(row: Row) -> str:
    return "adult" if row["age"] >= 18 else "minor"

def to_out(row: Row) -> Out:
    return {
        "name": row["name"],
        "age": row["age"],
        "email": row["email"],
        "segment": segment(row),
    }

def core_pipeline(records: Iterable[Raw]) -> Iterator[Out]:
    for raw in records:
        r_norm = normalize(raw) 
        v = validate_all(r_norm) 
        if isinstance(v, Ok):
            yield to_out(v.value)

@dataclass(frozen=True)
class Report:
    oks: list[Out]
    errs: list[str]

def core_collect(records: Iterable[Raw]) -> Report:
    oks: list[Out] = []
    errs: list[str] = []
    for raw in records:
        r_norm = normalize(raw)
        v = validate_all(r_norm)
        
        if isinstance(v, Ok):
            oks.append(to_out(v.value))
        else:
            errs.append(v.error)
    return Report(oks=oks, errs=errs)

def _run_tests() -> None:
    demo: list[Raw] = [
        {"name":"   aLiCe  ", "age":"19", "country":" ua ", "email":"Alice@EXAMPLE.com"},
        {"name":"Bob",       "age":"17", "country":" IN",  "email":"bad_at"},
        {"name":"Carol",     "age":"21", "country":"IT",   "email":"c@ex.io"},
        {"name":"EmptyAge",  "age":"  ", "country":"UA",   "email":"fail@example.com"},
    ]
    
    n0_result = normalize(demo[0])
    assert isinstance(n0_result, Ok)
    n0 = n0_result.value
    
    assert n0 == {"name":"Alice","age":19,"country":"UA","email":"alice@example.com"}
    
    assert isinstance(validate_all(n0_result), Ok)
    
    assert isinstance(validate_all(normalize(demo[1])), Err)
    
    assert isinstance(validate_all(normalize(demo[3])), Err) 
    
    out = list(core_pipeline(demo))
    assert [r["name"] for r in out] == ["Alice", "Carol"] 
    assert out[0]["segment"] == "adult"
    print("✅ lab10_etl_core: тести пройдено.")

if __name__ == "__main__":
    _run_tests()