import pytest
from expr import Num, Add, Mul, Num2, Bin
from eval_ import eval_expr, eval_expr2, EvalOverflow
from pretty import render, render2

def test_eval_basic():
    assert eval_expr(Num(5)) == 5
    assert eval_expr(Add(Num(2), Num(3))) == 5
    assert eval_expr(Mul(Num(2), Num(3))) == 6

def test_eval_nested():
    ast = Mul(Add(Num(2), Num(3)), Num(4))  # (2+3)*4
    assert eval_expr(ast) == 20

def test_render():
    ast = Mul(Add(Num(2), Num(3)), Num(4))
    assert render(ast) == "((2 + 3) * 4)"

def test_overflow_guard():
    with pytest.raises(EvalOverflow):
        # (10001) should overflow with MAX_ABS = 10_000
        eval_expr(Num(10001))

def test_alt_ast_and_eval():
    e2 = Bin("*", Bin("+", Num2(2), Num2(3)), Num2(4))
    assert render2(e2) == "((2 + 3) * 4)"
    assert eval_expr2(e2) == 20
