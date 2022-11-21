import arithmetic
import gates
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


def test_alu_f_of_x_and_y_equals_zero():
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


def test_alu_f_of_x_and_y_equals_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = 1
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=True, ny=True, f=True, no=True
        )

        assert out == (False,) * 15 + (True,)
        assert zr == False
        assert ng == False


def test_alu_f_of_x_and_y_equals_negative_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = -1
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=True, ny=False, f=True, no=False
        )

        assert out == (True,) * 16
        assert zr == False
        assert ng == True


def test_alu_f_of_x_and_y_equals_x():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=True, ny=True, f=False, no=False
        )

        assert out == xs
        assert zr == all(o == False for o in out)
        assert ng == (xs[0] == True)


def test_alu_f_of_x_and_y_equals_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=False, ny=False, f=False, no=False
        )
        assert out == ys
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_not_x():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = !x
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=True, ny=True, f=False, no=True
        )
        assert out == gates.NOT16(xs)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_not_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = !y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=False, ny=False, f=False, no=True
        )
        assert out == gates.NOT16(ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_negative_x():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = -x
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=True, ny=True, f=True, no=True
        )
        assert out == arithmetic.INC16(gates.NOT16(xs))
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_negative_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = -y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=False, ny=False, f=True, no=True
        )
        assert out == arithmetic.INC16(gates.NOT16(ys))
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_plus_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x + 1
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=True, zy=True, ny=True, f=True, no=True
        )
        assert out == arithmetic.INC16(xs)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_y_plus_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = y + 1
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=False, ny=True, f=True, no=True
        )
        assert out == arithmetic.INC16(ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_minus_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x - 1
        minus_one = (True,) * 16
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=True, ny=True, f=True, no=False
        )
        assert out == arithmetic.ADD16(xs, minus_one)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_y_minus_one():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = y - 1
        minus_one = (True,) * 16
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=True, nx=True, zy=False, ny=False, f=True, no=False
        )
        assert out == arithmetic.ADD16(ys, minus_one)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_plus_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x + y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=False, ny=False, f=True, no=False
        )
        assert out == arithmetic.ADD16(xs, ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_minus_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x - y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=True, zy=False, ny=False, f=True, no=True
        )
        assert out == arithmetic.ADD16(xs, arithmetic.NEG16(ys))
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_y_minus_x():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = y - x
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=False, ny=True, f=True, no=True
        )
        assert out == arithmetic.ADD16(arithmetic.NEG16(xs), ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_and_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x & y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=False, zy=False, ny=False, f=False, no=False
        )
        assert out == gates.AND16(xs, ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)


def test_alu_f_of_x_and_y_equals_x_or_y():
    for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST):
        xs = utils.sample_bits(16)
        ys = utils.sample_bits(16)

        # f(x, y) = x | y
        out, zr, ng = arithmetic.ALU(
            xs, ys, zx=False, nx=True, zy=False, ny=True, f=False, no=True
        )
        assert out == gates.OR16(xs, ys)
        assert zr == all(o == False for o in out)
        assert ng == (out[0] == True)
