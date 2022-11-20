from gates import NOT16, OR16, MUX8WAY16
from typing import Tuple


def HALFADDER(x: bool, y: bool) -> Tuple[bool, bool]:
    """Adds up 2 bits."""
    # pre-conditions
    assert isinstance(x, bool)
    assert isinstance(y, bool)

    # implementation
    s = x or y
    carry = x and y
    out = s, carry

    # post-conditions
    assert isinstance(out, tuple)
    assert len(out) == 2
    assert all(isinstance(o, bool) for o in out)

    return out


def FULLADDER(x: bool, y: bool, carry: bool) -> Tuple[bool, bool]:
    """Adds up 3 bits."""
    # pre-conditions
    assert isinstance(x, bool)
    assert isinstance(y, bool)
    assert isinstance(carry, bool)

    # implementation
    fst_sum, fst_carry = HALFADDER(x, y)
    new_sum, snd_carry = HALFADDER(fst_sum, carry)
    new_carry = fst_carry or snd_carry
    out = new_sum, new_carry

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 2
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 2-tuple of `bool`s"

    return out


def ADD16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    """Adds up two 16-bit two's complement numbers. Overflow is ignored."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`x` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`y` must be a 16-tuple of `bool`s"

    # implementation
    out, carry = [False] * 16, False

    for i, (x, y) in enumerate(zip(xs[::-1], ys[::-1])):
        out[i], carry = FULLADDER(x, y, carry)

    out = tuple(out[::-1])

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "`out must be a 16-tuple of `bool`s"

    return out


def INC16(xs: Tuple[bool]) -> Tuple[bool]:
    """Adds 1 to input. Overflow is ignored."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be a 16-tuple of `bool`s"

    # implementation
    one = (False,) * 15 + (True,)
    out = ADD16(xs, one)

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "`out must be a 16-tuple of `bool`s"

    return out


def NEG16(xs: Tuple[bool]) -> Tuple[bool]:
    """Negates input."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be a 16-tuple of `bool`s"

    # implementation
    out = INC16(NOT16(xs))

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(x, bool) for x in out)
    ), "`out` must be a 16-tuple of `bool`s"

    return out


def ALU(
    xs: Tuple[bool],
    ys: Tuple[bool],
    zx: bool,
    nx: bool,
    zy: bool,
    ny: bool,
    f: bool,
    no: bool,
) -> Tuple[Tuple[bool], bool, bool]:
    """
    Performs arithmetic and logic operations on two 16-bit two's complement numbers. Overflow is ignored.

    Args:
        xs: 16-bit two's complement number
        ys: 16-bit two's complement number
        zx: if True, `xs` is set to 0
        nx: if True, `xs` is negated
        zy: if True, `ys` is set to 0
        ny: if True, `ys` is negated
        f: if True, `xs` and `ys` are added, otherwise they're anded
        no: if True, the output is negated

    Returns:
        out: 16-bit two's complement number
        zr: if True, `out` is 0
        ng: if True, `out` is negative
    """
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be a 16-tuple of `bool`s"
    assert isinstance(zx, bool), "`zx` must be a `bool`"
    assert isinstance(nx, bool), "`nx` must be a `bool`"
    assert isinstance(zy, bool), "`zy` must be a `bool`"
    assert isinstance(ny, bool), "`ny` must be a `bool`"
    assert isinstance(f, bool), "`f` must be a `bool`"
    assert isinstance(no, bool), "`no` must be a `bool`"

    # implementation
    out = OR16((((((zx and nx) and zy) and ny) and f) and no))
    zr = None
    ng = None

    MUX8WAY16()

    # post-conditions
    assert True

    return out, zr, ng
