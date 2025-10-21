import numpy as np
from gates_numpy import (
    AND,
    AND16,
    OR,
    OR16,
    OR8WAY,
    OR16WAY,
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
        assert np.array_equal(DMUX(x, sel=False), np.array([x, False]))
        assert np.array_equal(DMUX(x, sel=True), np.array([False, x]))


# 16-bit variants
def test_not16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = np.array(sample_bits(16), dtype=bool)
        result = NOT16(xs)
        for x, not_x in zip(xs, result):
            assert not_x == (not x)


def test_and16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = np.array(sample_bits(16), dtype=bool)
        ys = np.array(sample_bits(16), dtype=bool)
        result = AND16(xs, ys)
        for x, y, x_and_y in zip(xs, ys, result):
            assert x_and_y == (x and y)


def test_or16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = np.array(sample_bits(16), dtype=bool)
        ys = np.array(sample_bits(16), dtype=bool)
        result = OR16(xs, ys)
        for x, y, x_or_y in zip(xs, ys, result):
            assert x_or_y == (x or y)


def test_mux16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = np.array(sample_bits(16), dtype=bool)
        ys = np.array(sample_bits(16), dtype=bool)
        assert np.array_equal(MUX16(xs, ys, sel=False), xs)
        assert np.array_equal(MUX16(xs, ys, sel=True), ys)


# multi-way variants
def test_or8way():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs_tuple = sample_bits(8)
        xs = np.array(xs_tuple, dtype=bool)
        assert OR8WAY(xs) == any(xs_tuple)


def test_or16way():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs_tuple = sample_bits(16)
        xs = np.array(xs_tuple, dtype=bool)
        assert OR16WAY(xs) == any(xs_tuple)


def test_mux4way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [np.array(sample_bits(16), dtype=bool) for _ in range(4)]
        sel = np.array([False, False], dtype=bool)
        assert np.array_equal(MUX4WAY16(*xs, sel=sel), xs[0])
        sel = np.array([False, True], dtype=bool)
        assert np.array_equal(MUX4WAY16(*xs, sel=sel), xs[1])
        sel = np.array([True, False], dtype=bool)
        assert np.array_equal(MUX4WAY16(*xs, sel=sel), xs[2])
        sel = np.array([True, True], dtype=bool)
        assert np.array_equal(MUX4WAY16(*xs, sel=sel), xs[3])


def test_mux8way16():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = [np.array(sample_bits(16), dtype=bool) for _ in range(8)]
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([False, False, False], dtype=bool)), xs[0])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([False, False, True], dtype=bool)), xs[1])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([False, True, False], dtype=bool)), xs[2])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([False, True, True], dtype=bool)), xs[3])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([True, False, False], dtype=bool)), xs[4])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([True, False, True], dtype=bool)), xs[5])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([True, True, False], dtype=bool)), xs[6])
        assert np.array_equal(MUX8WAY16(*xs, sel=np.array([True, True, True], dtype=bool)), xs[7])


def test_dmux4way():
    for x in [True, False]:
        assert np.array_equal(DMUX4WAY(x, sel=np.array([False, False], dtype=bool)), np.array([x, False, False, False]))
        assert np.array_equal(DMUX4WAY(x, sel=np.array([False, True], dtype=bool)), np.array([False, x, False, False]))
        assert np.array_equal(DMUX4WAY(x, sel=np.array([True, False], dtype=bool)), np.array([False, False, x, False]))
        assert np.array_equal(DMUX4WAY(x, sel=np.array([True, True], dtype=bool)), np.array([False, False, False, x]))


def test_dmux8way():
    assert np.array_equal(DMUX8WAY(True, sel=np.array([False, False, False], dtype=bool)), np.array(make_one_hot(n=8, i=0)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([False, False, True], dtype=bool)), np.array(make_one_hot(n=8, i=1)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([False, True, False], dtype=bool)), np.array(make_one_hot(n=8, i=2)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([False, True, True], dtype=bool)), np.array(make_one_hot(n=8, i=3)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([True, False, False], dtype=bool)), np.array(make_one_hot(n=8, i=4)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([True, False, True], dtype=bool)), np.array(make_one_hot(n=8, i=5)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([True, True, False], dtype=bool)), np.array(make_one_hot(n=8, i=6)))
    assert np.array_equal(DMUX8WAY(True, sel=np.array([True, True, True], dtype=bool)), np.array(make_one_hot(n=8, i=7)))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([False, False, False], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([False, False, True], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([False, True, False], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([False, True, True], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([True, False, False], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([True, False, True], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([True, True, False], dtype=bool)), np.array([False] * 8))
    assert np.array_equal(DMUX8WAY(False, sel=np.array([True, True, True], dtype=bool)), np.array([False] * 8))
