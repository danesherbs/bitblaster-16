from utils import is_n_bit_vector


# elementary logic gates
def AND(x: bool, y: bool) -> bool:
    """And gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # body
    out = x and y

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def OR(x: bool, y: bool) -> bool:
    """Or gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # body
    out = x or y

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def NOT(x: bool) -> bool:
    """Not gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"

    # body
    out = not x

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def NAND(x: bool, y: bool) -> bool:
    """Nand gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # body
    out = not (x and y)

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def XOR(x: bool, y: bool) -> bool:
    """Xor gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # body
    out = ((not x) and y) or (x and (not y))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def MUX(x: bool, y: bool, sel: bool) -> bool:
    """Selects between two inputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body
    out = (
        (x and (not y) and (not sel))
        or (x and y and (not sel))
        or ((not x) and y and sel)
        or (x and y and sel)
    )

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def DMUX(x: bool, sel: bool) -> tuple[bool, bool]:
    """Channels the input to one out of two outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body
    out = (x and (not sel), x and sel)

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 2
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 2-tuple of `bool`s"

    return out


# 16-bit variants
def NOT16(xs: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit Not."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"

    # body
    out = tuple(not x for x in xs)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def AND16(xs: tuple[bool, ...], ys: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit And."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"

    # body
    out = tuple(x and y for x, y in zip(xs, ys))

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def OR16(xs: tuple[bool, ...], ys: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit Or."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"

    # body
    out = tuple(x or y for x, y in zip(xs, ys))

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def MUX16(xs: tuple[bool, ...], ys: tuple[bool, ...], sel: bool) -> tuple[bool, ...]:
    """Selects between two 16-bit inputs."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body
    out = tuple(MUX(x, y, sel) for x, y in zip(xs, ys))

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


# multi-way variants
def OR8WAY(xs: tuple[bool, ...]) -> bool:
    """8-way Or."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=8), "`xs` must be an 8-tuple of `bool`s"

    # body
    out = xs[0] or (
        xs[1] or (xs[2] or (xs[3] or (xs[4] or (xs[5] or (xs[6] or xs[7])))))
    )

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def OR16WAY(xs: tuple[bool, ...]) -> bool:
    """16-way Or."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be an 16-tuple of `bool`s"

    # body
    out = OR(OR8WAY(xs[:8]), OR8WAY(xs[8:]))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def MUX4WAY16(
    xs: tuple[bool, ...],
    ys: tuple[bool, ...],
    zs: tuple[bool, ...],
    ws: tuple[bool, ...],
    sel: tuple[bool, ...],
) -> tuple[bool, ...]:
    """Selects between four 16-bit inputs."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(zs, n=16), "`zs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ws, n=16), "`ws` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(sel, n=2), "`sel` must be a 2-tuple of `bool`s"

    # body
    out = MUX16(
        MUX16(
            MUX16(
                xs,
                ys,
                (not sel[0]) and sel[1],
            ),
            zs,
            sel[0] and (not sel[1]),
        ),
        ws,
        sel[0] and sel[1],
    )

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def MUX8WAY16(
    xs: tuple[bool, ...],
    ys: tuple[bool, ...],
    zs: tuple[bool, ...],
    ws: tuple[bool, ...],
    us: tuple[bool, ...],
    vs: tuple[bool, ...],
    ms: tuple[bool, ...],
    ns: tuple[bool, ...],
    sel: tuple[bool, ...],
) -> tuple[bool, ...]:
    """Selects between eight 16-bit inputs."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(zs, n=16), "`zs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ws, n=16), "`ws` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(us, n=16), "`us` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(vs, n=16), "`vs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ms, n=16), "`ms` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ns, n=16), "`ns` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(sel, n=3), "`sel` must be a 3-tuple of `bool`s"

    # body
    out = MUX16(
        MUX4WAY16(xs, ys, zs, ws, sel=(sel[1], sel[2])),
        MUX4WAY16(us, vs, ms, ns, sel=(sel[1], sel[2])),
        sel[0],
    )

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def DMUX4WAY(x: bool, sel: tuple[bool, ...]) -> tuple[bool, bool, bool, bool]:
    """Channels the input to one out of four outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert is_n_bit_vector(sel, n=2), "`sel` must be a 2-tuple of `bool`s"

    # body
    x1, x2 = DMUX(x, sel[1])
    x3, x4 = DMUX(x, sel[1])
    out = (
        ((not sel[0]) and (not sel[1])) and x1,
        ((not sel[0]) and sel[1]) and x2,
        (sel[0] and (not sel[1])) and x3,
        (sel[0] and sel[1]) and x4,
    )

    # post-conditions
    assert is_n_bit_vector(out, n=4), "Output must be a 4-tuple of `bool`s"

    return out


def DMUX8WAY(
    x: bool, sel: tuple[bool, ...]
) -> tuple[bool, bool, bool, bool, bool, bool, bool, bool]:
    """Channels the input to one out of eight outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert is_n_bit_vector(sel, n=3), "`sel` must be a 3-tuple of `bool`s"

    # body
    x1, x2, x3, x4 = DMUX4WAY(x, sel=(sel[1], sel[2]))
    x5, x6, x7, x8 = DMUX4WAY(x, sel=(sel[1], sel[2]))
    out = (
        (not sel[0]) and x1,
        (not sel[0]) and x2,
        (not sel[0]) and x3,
        (not sel[0]) and x4,
        sel[0] and x5,
        sel[0] and x6,
        sel[0] and x7,
        sel[0] and x8,
    )

    # post-conditions
    assert is_n_bit_vector(out, n=8), "Output must be a 8-tuple of `bool`s"

    return out
