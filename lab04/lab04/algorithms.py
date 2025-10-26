from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from random import choice
from typing import Generator, List, Optional


# ------------------- Quicksort (recursive, pure) -------------------
def quicksort(xs: List[int]) -> List[int]:
    """Functional quicksort with random pivot. Returns a new sorted list; does not mutate input."""
    n = len(xs)
    if n <= 1:
        return xs[:]
    p = choice(xs)
    left = [x for x in xs if x < p]
    mid = [x for x in xs if x == p]
    right = [x for x in xs if x > p]
    return quicksort(left) + mid + quicksort(right)


# ------------------- Binary tree and traversals -------------------
@dataclass(slots=True)
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def preorder(t: Optional[Node]) -> Generator[int, None, None]:
    if t is None:
        return
    yield t.key
    if t.left is not None:
        yield from preorder(t.left)
    if t.right is not None:
        yield from preorder(t.right)


def inorder(t: Optional[Node]) -> Generator[int, None, None]:
    if t is None:
        return
    if t.left is not None:
        yield from inorder(t.left)
    yield t.key
    if t.right is not None:
        yield from inorder(t.right)


def postorder(t: Optional[Node]) -> Generator[int, None, None]:
    if t is None:
        return
    if t.left is not None:
        yield from postorder(t.left)
    if t.right is not None:
        yield from postorder(t.right)
    yield t.key


# Iterative alternatives
def bfs_level_order(t: Optional[Node]) -> List[int]:
    if not t:
        return []
    q, out = deque([t]), []
    while q:
        n = q.popleft()
        out.append(n.key)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return out


def dfs_preorder_iter(t: Optional[Node]) -> List[int]:
    if not t:
        return []
    stack, out = [t], []
    while stack:
        n = stack.pop()
        out.append(n.key)
        if n.right:
            stack.append(n.right)
        if n.left:
            stack.append(n.left)
    return out


# ------------------- Memoized Fibonacci -------------------
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
