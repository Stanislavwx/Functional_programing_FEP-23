from __future__ import annotations

from typing import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    """Простий closure-лічильник (stateful closure).

    Демонструє, як внутрішня функція (inc) захоплює та модифікує
    змінну (value) з зовнішньої області видимості.
    """
    value = start
    def inc() -> int:
        nonlocal value  # Обов'язково для зміни вільної змінної
        value += 1
        return value
    return inc


def make_logger(prefix: str) -> Callable[[str], None]:
    """Логер із префіксом (Dependency Injection через замикання).

    Внутрішня функція (log) захоплює параметр (prefix) і використовує його.
    Це дозволяє створювати налаштовані логери.
    """
    def log(msg: str) -> None:
        print(f"[{prefix}] {msg}")
    return log