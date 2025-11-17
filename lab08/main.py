from expr import Num, Add, Mul, Num2, Bin
from eval_ import eval_expr, eval_expr2
from pretty import render, render2

# (2 + 3) * 4 = 20
e1 = Mul(Add(Num(2), Num(3)), Num(4))
print("AST:", render(e1))
print("eval:", eval_expr(e1))

# Alternative AST with Literal operator
e2 = Bin("*", Bin("+", Num2(2), Num2(3)), Num2(4))
print("AST2:", render2(e2))
print("eval2:", eval_expr2(e2))