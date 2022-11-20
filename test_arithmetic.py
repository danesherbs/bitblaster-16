import arithmetic
import utils

NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 1_000


def test_halfadder():
    assert arithmetic.HALFADDER(False, False) == (False, False)
    assert arithmetic.HALFADDER(False, True) == (True, False)
    assert arithmetic.HALFADDER(True, False) == (True, False)
    assert arithmetic.HALFADDER(True, True) == (False, True)


def test_fulladder():
    assert arithmetic.FULLADDER(False, False, False) == (False, False)
    assert arithmetic.FULLADDER(False, False, True) == (True, False)
    assert arithmetic.FULLADDER(False, True, False) == (True, False)
    assert arithmetic.FULLADDER(False, True, True) == (False, True)
    assert arithmetic.FULLADDER(True, False, False) == (True, False)
    assert arithmetic.FULLADDER(True, False, True) == (False, True)
    assert arithmetic.FULLADDER(True, True, False) == (False, True)
    assert arithmetic.FULLADDER(True, True, True) == (True, True)


def test_add16():
    assert arithmetic.ADD16((False,) * 16, (False,) * 16) == (False,) * 16
    assert arithmetic.ADD16((False,) * 16, (True,) * 16) == (True,) * 16
    assert arithmetic.ADD16((True,) * 16, (False,) * 16) == (True,) * 16
    assert arithmetic.ADD16((True,) * 16, (False,) * 15 + (True,)) == (False,) * 16


def test_inc16():
    assert arithmetic.INC16((False,) * 16) == (False,) * 15 + (True,)
    assert arithmetic.INC16((True,) * 16) == (False,) * 16
    assert arithmetic.INC16((True,) + (False,) * 15) == (True,) + (False,) * 14 + (
        True,
    )


def test_neg16():
    assert arithmetic.NEG16((False,) * 16) == (False,) * 16
    assert arithmetic.NEG16((True,) * 16) == (False,) * 15 + (True,)


def test_alu():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = 0
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=False, zy=True, ny=False, f=True, no=False
        )
        assert out == (False,) * 16
        assert zr == True
        assert ng == False

        # f(x, y) = 1
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=True, ny=True, f=True, no=True
        )
        assert out == (False,) * 15 + (True,)
        assert zr == False
        assert ng == False

        # f(x, y) = -1
        # assert (
        #     arithmetic.ALU(
        #         xs, ys, zx=True, nx=True, zy=True, ny=False, f=True, no=False
        #     )
        #     == (True,) * 16
        # )
