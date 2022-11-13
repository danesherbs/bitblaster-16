import gates
import random


def _sample_bits(n: int) -> tuple:
    """Returns a random `n`-bit tuple of bools."""
    assert n >= 0 and isinstance(n, int)
    return tuple(random.choice([True, False]) for _ in range(n))


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

        for x, y, out in zip(xs, ys, gates.MUX16(xs, ys, sel=False)):
            assert out == x

        for x, y, out in zip(xs, ys, gates.MUX16(xs, ys, sel=True)):
            assert out == y


# multi-way variants
def test_or8way():
    for _ in range(100):
        xs = _sample_bits(8)
        assert gates.OR8WAY(xs) == any(xs)


def test_mux4way16():
    for _ in range(100):
        xs = _sample_bits(16)
        ys = _sample_bits(16)
        zs = _sample_bits(16)
        ws = _sample_bits(16)

        for x, y, z, w, out in zip(
            xs, ys, zs, ws, gates.MUX4WAY16(xs, ys, zs, ws, sel=(False, False))
        ):
            assert out == x

        for x, y, z, w, out in zip(
            xs, ys, zs, ws, gates.MUX4WAY16(xs, ys, zs, ws, sel=(False, True))
        ):
            assert out == y

        for x, y, z, w, out in zip(
            xs, ys, zs, ws, gates.MUX4WAY16(xs, ys, zs, ws, sel=(True, False))
        ):
            assert out == z

        for x, y, z, w, out in zip(
            xs, ys, zs, ws, gates.MUX4WAY16(xs, ys, zs, ws, sel=(True, True))
        ):
            assert out == w


def test_mux8way16():
    for _ in range(100):
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
    raise NotImplementedError()


def test_dmux8way():
    raise NotImplementedError()
