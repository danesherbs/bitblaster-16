from gates import NOT, NOT16, AND16, OR16WAY, XOR, AND, MUX16
from typing import Tuple
from utils import is_n_bit_vector


ZERO16 = (False,) * 16


def HALFADDER(x: bool, y: bool) -> tuple[bool, bool]:
    """Adds up 2 bits."""
    # pre-conditions
    assert isinstance(x, bool)
    assert isinstance(y, bool)

    # implementation
    s = XOR(x, y)
    carry = AND(x, y)
    out = s, carry

    # post-conditions
    assert is_n_bit_vector(out, n=2)

    return out


def FULLADDER(x: bool, y: bool, carry: bool) -> tuple[bool, bool]:
    """Adds up 3 bits."""
    # pre-conditions
    assert isinstance(x, bool)
    assert isinstance(y, bool)
    assert isinstance(carry, bool)

    # implementation
    fst_sum, fst_carry = HALFADDER(x, y)
    snd_sum, snd_carry = HALFADDER(fst_sum, carry)

    new_sum = snd_sum
    new_carry = fst_carry or snd_carry

    out = new_sum, new_carry

    # post-conditions
    assert is_n_bit_vector(out, n=2), "Output must be 2-tuple of `bool`s"

    return out


def ADD16(xs: tuple[bool, ...], ys: tuple[bool, ...]) -> tuple[bool, ...]:
    """Adds up two 16-bit two's complement numbers. Overflow is ignored."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`x` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`y` must be a 16-tuple of `bool`s"

    # implementation
    out, carry = [False] * 16, False

    for i, (x, y) in enumerate(zip(xs[::-1], ys[::-1])):
        out[i], carry = FULLADDER(x, y, carry)

    out = tuple(out[::-1])  # type: ignore

    # post-conditions
    assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"

    return out  # type: ignore


def INC16(xs: tuple[bool, ...]) -> tuple[bool, ...]:
    """Adds 1 to input. Overflow is ignored."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"

    # implementation
    one = (False,) * 15 + (True,)
    out = ADD16(xs, one)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"

    return out


def NEG16(xs: tuple[bool, ...]) -> tuple[bool, ...]:
    """Negates input."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"

    # implementation
    out = INC16(NOT16(xs))

    # post-conditions
    assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"

    return out


def _PRESET16(xs: tuple[bool, ...], zx: bool, nx: bool) -> tuple[bool, ...]:
    """Prepares input for ALU. Zeroes out input if `zx` is `True` then negates input if `nx` is `True`."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
    assert isinstance(zx, bool), "`zx` must be a `bool`"
    assert isinstance(nx, bool), "`nx` must be a `bool`"

    # implementation
    zeroed = MUX16(
        xs,
        ZERO16,
        zx,
    )

    out = MUX16(
        zeroed,
        NOT16(zeroed),
        nx,
    )

    # post-conditions
    assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"

    return out


def ALU(
    xs: tuple[bool, ...],
    ys: tuple[bool, ...],
    zx: bool,
    nx: bool,
    zy: bool,
    ny: bool,
    f: bool,
    no: bool,
) -> tuple[tuple[bool, ...], bool, bool]:
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
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be a 16-tuple of `bool`s"
    assert isinstance(zx, bool), "`zx` must be a `bool`"
    assert isinstance(nx, bool), "`nx` must be a `bool`"
    assert isinstance(zy, bool), "`zy` must be a `bool`"
    assert isinstance(ny, bool), "`ny` must be a `bool`"
    assert isinstance(f, bool), "`f` must be a `bool`"
    assert isinstance(no, bool), "`no` must be a `bool`"

    # implementation
    tx = _PRESET16(xs, zx, nx)
    ty = _PRESET16(ys, zy, ny)

    out = MUX16(
        AND16(tx, ty),
        ADD16(tx, ty),
        f,
    )

    tout = MUX16(
        out,
        NOT16(out),
        no,
    )

    zr = NOT(OR16WAY(tout))
    ng = tout[0]

    # post-conditions
    assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"
    assert isinstance(zr, bool), "`zr` must be a `bool`"
    assert isinstance(ng, bool), "`ng` must be a `bool`"

    return tout, zr, ng
