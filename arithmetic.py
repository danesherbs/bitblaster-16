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


def ADD16(x: Tuple[bool], y: Tuple[bool]) -> Tuple[bool]:
    pass


def INC16(x: Tuple[bool]) -> Tuple[bool]:
    pass
