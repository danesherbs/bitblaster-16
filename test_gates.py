from gates import (
    AND,
    AND16,
    OR,
    OR16,
    OR8WAY,
    NOT,
    NOT16,
    NAND,
    XOR,
    MUX,
    MUX16,
    MUX4WAY16,
    MUX8WAY16,
    DMUX,
    DMUX4WAY,
    DMUX8WAY,
)

from utils import make_one_hot, sample_bits


NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 1_024


# elementary logic gates
def test_and():
    assert AND(False, False) == False
    assert AND(False, True) == False
    assert AND(True, False) == False
    assert AND(True, True) == True


def test_or():
    assert OR(False, False) == False
    assert OR(False, True) == True
    assert OR(True, False) == True
    assert OR(True, True) == True


def test_not():
    assert NOT(False) == True
    assert NOT(True) == False


def test_nand():
    assert NAND(False, False) == True
    assert NAND(False, True) == True
    assert NAND(True, False) == True
    assert NAND(True, True) == False


def test_xor():
    assert XOR(False, False) == False
    assert XOR(False, True) == True
    assert XOR(True, False) == True
    assert XOR(True, True) == False


def test_mux():
    for x in [True, False]:
        for y in [True, False]:
            assert MUX(x, y, sel=False) == x
            assert MUX(x, y, sel=True) == y


def test_dmux():
    for x in [True, False]:
        assert DMUX(x, sel=False) == (x, False)
        assert DMUX(x, sel=True) == (False, x)


# 16-bit variants
def test_not16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = sample_bits(16)
        for x, not_x in zip(xs, NOT16(xs)):
            assert not_x == (not x)


def test_and16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = sample_bits(16)
        ys = sample_bits(16)
        for x, y, x_and_y in zip(xs, ys, AND16(xs, ys)):
            assert x_and_y == (x and y)


def test_or16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = sample_bits(16)
        ys = sample_bits(16)
        for x, y, x_or_y in zip(xs, ys, OR16(xs, ys)):
            assert x_or_y == (x or y)


def test_mux16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = sample_bits(16)
        ys = sample_bits(16)
        assert MUX16(xs, ys, sel=False) == xs
        assert MUX16(xs, ys, sel=True) == ys


# multi-way variants
def test_or8way():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = sample_bits(8)
        assert OR8WAY(xs) == any(xs)


def test_mux4way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [sample_bits(16) for _ in range(4)]
        assert MUX4WAY16(*xs, sel=(False, False)) == xs[0]
        assert MUX4WAY16(*xs, sel=(False, True)) == xs[1]
        assert MUX4WAY16(*xs, sel=(True, False)) == xs[2]
        assert MUX4WAY16(*xs, sel=(True, True)) == xs[3]


def test_mux8way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [sample_bits(16) for _ in range(8)]
        assert MUX8WAY16(*xs, sel=(False, False, False)) == xs[0]
        assert MUX8WAY16(*xs, sel=(False, False, True)) == xs[1]
        assert MUX8WAY16(*xs, sel=(False, True, False)) == xs[2]
        assert MUX8WAY16(*xs, sel=(False, True, True)) == xs[3]
        assert MUX8WAY16(*xs, sel=(True, False, False)) == xs[4]
        assert MUX8WAY16(*xs, sel=(True, False, True)) == xs[5]
        assert MUX8WAY16(*xs, sel=(True, True, False)) == xs[6]
        assert MUX8WAY16(*xs, sel=(True, True, True)) == xs[7]


def test_dmux4way():
    for x in [True, False]:
        assert DMUX4WAY(x, sel=(False, False)) == (x, False, False, False)
        assert DMUX4WAY(x, sel=(False, True)) == (False, x, False, False)
        assert DMUX4WAY(x, sel=(True, False)) == (False, False, x, False)
        assert DMUX4WAY(x, sel=(True, True)) == (False, False, False, x)


def test_dmux8way():
    assert DMUX8WAY(True, sel=(False, False, False)) == make_one_hot(n=8, i=0)
    assert DMUX8WAY(True, sel=(False, False, True)) == make_one_hot(n=8, i=1)
    assert DMUX8WAY(True, sel=(False, True, False)) == make_one_hot(n=8, i=2)
    assert DMUX8WAY(True, sel=(False, True, True)) == make_one_hot(n=8, i=3)
    assert DMUX8WAY(True, sel=(True, False, False)) == make_one_hot(n=8, i=4)
    assert DMUX8WAY(True, sel=(True, False, True)) == make_one_hot(n=8, i=5)
    assert DMUX8WAY(True, sel=(True, True, False)) == make_one_hot(n=8, i=6)
    assert DMUX8WAY(True, sel=(True, True, True)) == make_one_hot(n=8, i=7)
    assert DMUX8WAY(False, sel=(False, False, False)) == (False,) * 8
    assert DMUX8WAY(False, sel=(False, False, True)) == (False,) * 8
    assert DMUX8WAY(False, sel=(False, True, False)) == (False,) * 8
    assert DMUX8WAY(False, sel=(False, True, True)) == (False,) * 8
    assert DMUX8WAY(False, sel=(True, False, False)) == (False,) * 8
    assert DMUX8WAY(False, sel=(True, False, True)) == (False,) * 8
    assert DMUX8WAY(False, sel=(True, True, False)) == (False,) * 8
    assert DMUX8WAY(False, sel=(True, True, True)) == (False,) * 8
