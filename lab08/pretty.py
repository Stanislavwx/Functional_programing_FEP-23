from __future__ import annotations
from expr import Expr, Num, Add, Mul, Expr2, Num2, Bin

def render(e: "Expr") -> str:
    match e:
        case Num(value=v):
            return str(v)
        case Add(left=a, right=b):
            return f"({render(a)} + {render(b)})"
        case Mul(left=a, right=b):
            return f"({render(a)} * {render(b)})"

def render2(e: "Expr2") -> str:
    match e:
        case Num2(value=v):
            return str(v)
        case Bin(op="+", left=a, right=b):
            return f"({render2(a)} + {render2(b)})"
        case Bin(op="*", left=a, right=b):
            return f"({render2(a)} * {render2(b)})"
