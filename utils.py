import random
from typing import Any


def sample_bits(n: int) -> tuple:
    """Returns a random `n`-bit tuple of bools."""
    # pre-conditions
    assert n >= 0 and isinstance(n, int), "`n` must be a non-negative integer"

    # body
    out = tuple(random.choice([True, False]) for _ in range(n))

    # post-conditions
    assert is_n_bit_vector(out, n), "output must be an `n`-bit tuple of bools"

    return out


def make_one_hot(n: int, i: int) -> tuple:
    """Returns an `n`-bit tuple of bools with a single `True` at index `i`."""
    # pre-conditions
    assert n >= 1 and isinstance(n, int), "`n` must be a positive integer"
    assert i >= 0 and i < n and isinstance(i, int), "`i` must be an integer in [0, n)"

    # body
    out = tuple(j == i for j in range(n))

    # post-conditions
    assert is_n_bit_vector(out, n), "output must be an `n`-bit tuple of bools"

    return out


def is_n_bit_vector(xs: Any, n: int) -> bool:
    """Returns `True` iff `xs` is a tuple of bools of length `n`."""
    if not isinstance(xs, tuple):
        return False
    
    if len(xs) != n:
        return False
    
    if not all(isinstance(b, bool) for b in xs):
        return False

    return True


def to_int(bs: tuple[bool, ...]) -> int:
    """Converts a tuple of boolean values into an integer."""
    # pre-conditions
    assert isinstance(bs, tuple), "input must be a tuple"
    assert all(isinstance(b, bool) for b in bs), "input must be a tuple of bools"

    # body
    int_values = [int(value) for value in bs]
    str_values = [str(value) for value in int_values]
    binary_repr = "".join(str_values)
    out = int(binary_repr, 2)

    # post-conditions
    assert isinstance(out, int), "output must be an integer"
    
    return out
