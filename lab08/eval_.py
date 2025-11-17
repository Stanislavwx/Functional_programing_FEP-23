from __future__ import annotations
from typing import Final
from expr import Expr, Num, Add, Mul, Expr2, Num2, Bin

# Simple overflow guard (demo of an invariant)
MAX_ABS: Final[int] = 10_000

class EvalOverflow(ValueError):
    pass

def _check_range(x: int) -> int:
    if abs(x) > MAX_ABS:
        raise EvalOverflow(f"overflow: {x}")
    return x

def eval_expr(e: "Expr") -> int:
    match e:
        case Num(value=v):
            return _check_range(v)
        case Add(left=a, right=b):
            return _check_range(eval_expr(a) + eval_expr(b))
        case Mul(left=a, right=b):
            return _check_range(eval_expr(a) * eval_expr(b))

# Alternative evaluator for the Literal/Op variant
def eval_expr2(e: "Expr2") -> int:
    match e:
        case Num2(value=v):
            return _check_range(v)
        case Bin(op="+", left=a, right=b):
            return _check_range(eval_expr2(a) + eval_expr2(b))
        case Bin(op="*", left=a, right=b):
            return _check_range(eval_expr2(a) * eval_expr2(b))
