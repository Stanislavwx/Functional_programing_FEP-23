from __future__ import annotations

import functools
import random
import threading
import time
from typing import Any, Callable, Hashable, Tuple, TypeVar, ParamSpec

# Використовуємо ParamSpec та TypeVar для збереження оригінальної сигнатури
P = ParamSpec("P")
R = TypeVar("R")

__all__ = ["timed", "retries", "cached"]


# Допоміжна функція для створення хешованого ключа кешу
def _make_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Hashable:
    """Створює хешований ключ з позиційних та іменованих аргументів."""
    # kwargs сортуються для забезпечення однакового ключа
    return (args, tuple(sorted(kwargs.items())))


# -----------------------------
# timed: параметризований декоратор таймінгу
# -----------------------------

def timed(
        label: str | None = None,
        *,
        unit: str = "ms",
        logger: Callable[[str], None] = print,
        clock: Callable[[], float] = time.perf_counter,  # Інʼєкція для тестів
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Вимірює час виконання функції і логує результат."""
    factors = {"s": 1.0, "ms": 1e3, "us": 1e6}
    if unit not in factors:
        raise ValueError("unit must be 's', 'ms', or 'us'")
    factor = factors[unit]

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label or func.__name__

        @functools.wraps(func)  # Зберігає ім'я, докстрінг, сигнатуру
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = clock()
            try:
                return func(*args, **kwargs)
            finally:  # Гарантує лог навіть при винятку
                dt = (clock() - t0) * factor
                logger(f"[timed] {name} took {dt:.3f} {unit}")

        return wrapper

    return decorator


# -----------------------------
# retries: повтор виклику при винятках
# -----------------------------

def retries(
        attempts: int = 3,
        exceptions: Tuple[type[BaseException], ...] = (Exception,),
        delay: float = 0.0,
        backoff: float = 1.0,  # >1.0 для експоненційного бекофу
        jitter: float = 0.0,
        *,
        sleep: Callable[[float], None] = time.sleep,  # Інʼєкція для тестів
        logger: Callable[[str], None] = lambda _: None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Повторює виклик при вказаних винятках із затримкою та бекофом."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if i == attempts:
                        logger(f"[retries] fail after {i} attempts: {e!r}")
                        break

                    # Обчислення експоненційного бекофу
                    wait = delay * (backoff ** (i - 1))
                    if jitter:
                        wait += random.random() * jitter

                    logger(f"[retries] attempt {i} failed: {e!r}; sleeping {wait:.3f}s")
                    sleep(wait)

            assert last_exc is not None  # Це має спрацювати лише якщо цикл завершився без успіху
            raise last_exc

        return wrapper

    return decorator


# -----------------------------
# cached: кеш із TTL та інвалідацією
# -----------------------------

def cached(
        *,
        ttl: float | None = None,  # Сек; None = безстроково
        time_fn: Callable[[], float] = time.time,  # Інʼєкція для тестів TTL
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Кешує значення функції з опційним TTL і методами інвалідації."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # Кеш: {key: (expiry_timestamp | None, result)}
        cache: dict[Hashable, tuple[float | None, R]] = {}
        lock = threading.Lock()  # Для багатопотокової безпеки [cite: 251]

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                key = _make_key(args, kwargs)
            except TypeError as e:
                # Обробка не-хешованих аргументів, якщо _make_key не справляється
                raise TypeError(f"Cannot cache non-hashable arguments: {e}") from e

            now = time_fn()

            # Перевірка кешу під локом
            with lock:
                if key in cache:
                    exp, val = cache[key]
                    if exp is None or now < exp:
                        return val
                    # Протухло: видалимо
                    del cache[key]

            # Обчислюємо значення поза локом, щоб не тримати блокування
            val = func(*args, **kwargs)

            # Запис у кеш під локом
            with lock:
                expiry = None if ttl is None else now + ttl
                cache[key] = (expiry, val)
            return val

        # ——— Методи очищення/інвалідації, що додаються до wrapper:
        def cache_clear() -> None:
            """Повне очищення кешу."""
            with lock:
                cache.clear()

        def cache_invalidate(predicate: Callable[[tuple[Any, ...], dict[str, Any]], bool]) -> int:
            """Часткове очищення кешу за предикатом."""
            removed = 0
            with lock:
                # Ітеруємося по копії ключів
                for k in list(cache.keys()):
                    # k[0] — args, k[1] — sorted(kwargs.items())
                    k_args, k_kwargs = k[0], dict(k[1])
                    if predicate(k_args, k_kwargs):
                        del cache[k]
                        removed += 1
            return removed

        # Додавання методів до обгортки [cite: 183-184]
        setattr(wrapper, "cache_clear", cache_clear)
        setattr(wrapper, "cache_invalidate", cache_invalidate)
        return wrapper

    return decorator