import gates
import random


NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 1_000


def _sample_bits(n: int) -> tuple:
    """Returns a random `n`-bit tuple of bools."""
    assert n >= 0 and isinstance(n, int), "`n` must be a non-negative integer"
    out = tuple(random.choice([True, False]) for _ in range(n))
    assert (
        isinstance(out, tuple)
        and len(out) == n
        and all(isinstance(x, bool) for x in out)
    ), "output must be an `n`-bit tuple of bools"
    return out


def _make_one_hot(n: int, i: int) -> tuple:
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


# elementary logic gates
def test_and():
    assert gates.AND(False, False) == False
    assert gates.AND(False, True) == False
    assert gates.AND(True, False) == False
    assert gates.AND(True, True) == True


def test_or():
    assert gates.OR(False, False) == False
    assert gates.OR(False, True) == True
    assert gates.OR(True, False) == True
    assert gates.OR(True, True) == True


def test_not():
    assert gates.NOT(False) == True
    assert gates.NOT(True) == False


def test_nand():
    assert gates.NAND(False, False) == True
    assert gates.NAND(False, True) == True
    assert gates.NAND(True, False) == True
    assert gates.NAND(True, True) == False


def test_xor():
    assert gates.XOR(False, False) == False
    assert gates.XOR(False, True) == True
    assert gates.XOR(True, False) == True
    assert gates.XOR(True, True) == False


def test_mux():
    for x in [True, False]:
        for y in [True, False]:
            assert gates.MUX(x, y, sel=True) == y
            assert gates.MUX(x, y, sel=False) == x


def test_dmux():
    for x in [True, False]:
        assert gates.DMUX(x, sel=False) == (x, False)
        assert gates.DMUX(x, sel=True) == (False, x)


# 16-bit variants
def test_not16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = _sample_bits(16)
        for x, not_x in zip(xs, gates.NOT16(xs)):
            assert not_x == (not x)


def test_and16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        for x, y, x_and_y in zip(xs, ys, gates.AND16(xs, ys)):
            assert x_and_y == (x and y)


def test_or16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        for x, y, x_or_y in zip(xs, ys, gates.OR16(xs, ys)):
            assert x_or_y == (x or y)


def test_mux16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = _sample_bits(16)
        ys = _sample_bits(16)

        for x, y, out in zip(xs, ys, gates.MUX16(xs, ys, sel=False)):
            assert out == x

        for x, y, out in zip(xs, ys, gates.MUX16(xs, ys, sel=True)):
            assert out == y


# multi-way variants
def test_or8way():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = _sample_bits(8)
        assert gates.OR8WAY(xs) == any(xs)


def test_mux4way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [_sample_bits(16) for _ in range(4)]
        assert gates.MUX4WAY16(*xs, sel=(False, False)) == xs[0]
        assert gates.MUX4WAY16(*xs, sel=(False, True)) == xs[1]
        assert gates.MUX4WAY16(*xs, sel=(True, False)) == xs[2]
        assert gates.MUX4WAY16(*xs, sel=(True, True)) == xs[3]


def test_mux8way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [_sample_bits(16) for _ in range(8)]
        assert gates.MUX8WAY16(*xs, sel=(False, False, False)) == xs[0]
        assert gates.MUX8WAY16(*xs, sel=(False, False, True)) == xs[1]
        assert gates.MUX8WAY16(*xs, sel=(False, True, False)) == xs[2]
        assert gates.MUX8WAY16(*xs, sel=(False, True, True)) == xs[3]
        assert gates.MUX8WAY16(*xs, sel=(True, False, False)) == xs[4]
        assert gates.MUX8WAY16(*xs, sel=(True, False, True)) == xs[5]
        assert gates.MUX8WAY16(*xs, sel=(True, True, False)) == xs[6]
        assert gates.MUX8WAY16(*xs, sel=(True, True, True)) == xs[7]


def test_dmux4way():
    for x in [True, False]:
        assert gates.DMUX4WAY(x, sel=(False, False)) == (x, False, False, False)
        assert gates.DMUX4WAY(x, sel=(False, True)) == (False, x, False, False)
        assert gates.DMUX4WAY(x, sel=(True, False)) == (False, False, x, False)
        assert gates.DMUX4WAY(x, sel=(True, True)) == (False, False, False, x)


def test_dmux8way():
    for x in [True, False]:
        assert gates.DMUX8WAY(x, sel=(False, False, False)) == _make_one_hot(n=8, i=0)
        assert gates.DMUX8WAY(x, sel=(False, False, True)) == _make_one_hot(n=8, i=1)
        assert gates.DMUX8WAY(x, sel=(False, True, False)) == _make_one_hot(n=8, i=2)
        assert gates.DMUX8WAY(x, sel=(False, True, True)) == _make_one_hot(n=8, i=3)
        assert gates.DMUX8WAY(x, sel=(True, False, False)) == _make_one_hot(n=8, i=4)
        assert gates.DMUX8WAY(x, sel=(True, False, True)) == _make_one_hot(n=8, i=5)
        assert gates.DMUX8WAY(x, sel=(True, True, False)) == _make_one_hot(n=8, i=6)
        assert gates.DMUX8WAY(x, sel=(True, True, True)) == _make_one_hot(n=8, i=7)
