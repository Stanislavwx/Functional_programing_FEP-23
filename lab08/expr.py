from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias, Literal, Protocol, Union

# --- Core AST -------------------------------------------------------------

@dataclass(frozen=True)
class Num:
    value: int

@dataclass(frozen=True)
class Add:
    left: "Expr"
    right: "Expr"

@dataclass(frozen=True)
class Mul:
    left: "Expr"
    right: "Expr"

# Type alias (Python 3.10–3.11 style; on 3.12+ you can use: `type Expr = ...`)
Expr: TypeAlias = Num | Add | Mul

# Optional: enable positional matching (case Add(l, r)) in addition to named fields
Num.__match_args__ = ("value",)
Add.__match_args__ = ("left", "right")
Mul.__match_args__ = ("left", "right")

# --- Alternative AST using Literal and a single binary node ----------------

Op: TypeAlias = Literal["+", "*"]

@dataclass(frozen=True)
class Bin:
    op: Op
    left: "Expr2"
    right: "Expr2"

@dataclass(frozen=True)
class Num2:
    value: int

Expr2: TypeAlias = Union[Num2, Bin]

class SupportsBin(Protocol):
    op: Op
    left: "Expr2"
    right: "Expr2"
