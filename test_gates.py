import gates
import random


def _sample_bits(n: int) -> tuple:
    """Returns a random `n`-bit tuple of bools."""
    assert n >= 0 and isinstance(n, int)
    return tuple(random.choice([True, False]) for _ in range(n))


# elementary logic gates
def test_and():
    assert gates.AND(0, 0) == 0
    assert gates.AND(0, 1) == 0
    assert gates.AND(1, 0) == 0
    assert gates.AND(1, 1) == 1

def test_or():
    assert gates.OR(0, 0) == 0
    assert gates.OR(0, 1) == 1
    assert gates.OR(1, 0) == 1
    assert gates.OR(1, 1) == 1

def test_not():
    assert gates.NOT(0) == 1
    assert gates.NOT(1) == 0

def test_nand():
    assert gates.NAND(0, 0) == 1
    assert gates.NAND(0, 1) == 1
    assert gates.NAND(1, 0) == 1
    assert gates.NAND(1, 1) == 0

def test_xor():
    assert gates.XOR(0, 0) == 0
    assert gates.XOR(0, 1) == 1
    assert gates.XOR(1, 0) == 1
    assert gates.XOR(1, 1) == 0

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
    for _ in range(100):
        xs = _sample_bits(16)
        for x, not_x in zip(xs, gates.NOT16(xs)):
            assert not_x == (not x)

def test_and16():
    for _ in range(100):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        for x, y, x_and_y in zip(xs, ys, gates.AND16(xs, ys)):
            assert x_and_y == (x and y)

def test_or16():
    for _ in range(100):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        for x, y, x_or_y in zip(xs, ys, gates.OR16(xs, ys)):
            assert x_or_y == (x or y)

def test_mux16():
    for _ in range(100):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        
        for x, y, x_or_y in zip(xs, ys, gates.MUX16(xs, ys, sel=False)):
            assert x_or_y == x

        for x, y, x_or_y in zip(xs, ys, gates.MUX16(xs, ys, sel=True)):
            assert x_or_y == y


# multi-way variants
def test_or8way():
    for _ in range(100):
        xs = _sample_bits(8)
        assert gates.OR8WAY(xs) == any(xs)

def test_mux4way16():
    raise NotImplementedError()

def test_mux8way16():
    raise NotImplementedError()

def test_dmux4way():
    raise NotImplementedError()

def test_dmux8way():
    raise NotImplementedError()
