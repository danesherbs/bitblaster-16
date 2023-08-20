import random
from typing import Any


def sample_bits(n: int) -> tuple:
    """Returns a random `n`-bit tuple of bools."""
    assert n >= 0 and isinstance(n, int), "`n` must be a non-negative integer"
    out = tuple(random.choice([True, False]) for _ in range(n))
    assert (
        isinstance(out, tuple)
        and len(out) == n
        and all(isinstance(x, bool) for x in out)
    ), "output must be an `n`-bit tuple of bools"
    return out


def make_one_hot(n: int, i: int) -> tuple:
    """Returns an `n`-bit tuple of bools with a single `True` at index `i`."""
    assert n >= 1 and isinstance(n, int), "`n` must be a positive integer"
    assert i >= 0 and i < n and isinstance(i, int), "`i` must be an integer in [0, n)"
    out = tuple(j == i for j in range(n))
    assert (
        isinstance(out, tuple)
        and len(out) == n
        and all(isinstance(x, bool) for x in out)
    ), "output must be an `n`-bit tuple of bools"
    return out

def is_n_bit_vector(xs: Any, n: int) -> bool:
    """Returns `True` iff `xs` is a tuple of bools of length `n`."""
    return isinstance(xs, tuple) and len(xs) == n and all(isinstance(b, bool) for b in xs)