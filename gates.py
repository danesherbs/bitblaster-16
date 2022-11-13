from typing import Tuple


# elementary logic gates
def AND(x: bool, y: bool) -> bool:
    """And gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # implementation
    out = x and y

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def OR(x: bool, y: bool) -> bool:
    """Or gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # implementation
    out = x or y

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def NOT(x: bool) -> bool:
    """Not gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"

    # implementation
    out = not x

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def NAND(x: bool, y: bool) -> bool:
    """Nand gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # implementation
    out = not (x and y)

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def XOR(x: bool, y: bool) -> bool:
    """Xor gate."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # implementation
    out = ((not x) and y) or (x and (not y))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def MUX(x: bool, y: bool, sel: bool) -> bool:
    """Selects between two inputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(y, bool), "`y` must be of type `bool`"

    # implementation
    out = (
        (x and (not y) and (not sel))
        or (x and y and (not sel))
        or ((not x) and y and sel)
        or (x and y and sel)
    )

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def DMUX(x: bool, sel: bool) -> Tuple[bool, bool]:
    """Channels the input to one out of two outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # implementation
    out = (x and (not sel), x and sel)

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 2
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 2-tuple of `bool`s"

    return out


# 16-bit variants
def NOT16(xs: Tuple[bool]) -> Tuple[bool]:
    """16-bit Not."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be 16-tuple of `bool`s"

    # implementation
    out = tuple(not x for x in xs)

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


def AND16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    """16-bit And."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be 16-tuple of `bool`s"

    # implementation
    out = tuple(x and y for x, y in zip(xs, ys))

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


def OR16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    """16-bit Or."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be 16-tuple of `bool`s"

    # implementation
    out = tuple(x or y for x, y in zip(xs, ys))

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


def MUX16(xs: Tuple[bool], ys: Tuple[bool], sel: bool) -> Tuple[bool]:
    """Selects between two 16-bit inputs."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be 16-tuple of `bool`s"

    # implementation
    out = tuple(MUX(x, y, sel) for x, y in zip(xs, ys))

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


# multi-way variants
def OR8WAY(xs: Tuple[bool]) -> bool:
    """8-way Or."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 8 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be an 8-tuple of `bool`s"

    # implementation
    out = xs[0] or (
        xs[1] or (xs[2] or (xs[3] or (xs[4] or (xs[5] or (xs[6] or xs[7])))))
    )

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def MUX4WAY16(
    xs: Tuple[bool], ys: Tuple[bool], zs: Tuple[bool], ws: Tuple[bool], sel: Tuple[bool]
) -> Tuple[bool]:
    """Selects between four 16-bit inputs."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be a 16-tuple of `bool`s"
    assert (
        isinstance(zs, tuple) and len(zs) == 16 and all(isinstance(z, bool) for z in zs)
    ), "`zs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ws, tuple) and len(ws) == 16 and all(isinstance(w, bool) for w in ws)
    ), "`ws` must be a 16-tuple of `bool`s"
    assert (
        isinstance(sel, tuple)
        and len(sel) == 2
        and all(isinstance(s, bool) for s in sel)
    ), "`sel` must be a 2-tuple of `bool`s"

    # implementation
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
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


def MUX8WAY16(
    xs: Tuple[bool],
    ys: Tuple[bool],
    zs: Tuple[bool],
    ws: Tuple[bool],
    us: Tuple[bool],
    vs: Tuple[bool],
    ms: Tuple[bool],
    ns: Tuple[bool],
    sel: Tuple[bool],
) -> Tuple[bool]:
    """Selects between eight 16-bit inputs."""
    # pre-conditions
    assert (
        isinstance(xs, tuple) and len(xs) == 16 and all(isinstance(x, bool) for x in xs)
    ), "`xs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ys, tuple) and len(ys) == 16 and all(isinstance(y, bool) for y in ys)
    ), "`ys` must be a 16-tuple of `bool`s"
    assert (
        isinstance(zs, tuple) and len(zs) == 16 and all(isinstance(z, bool) for z in zs)
    ), "`zs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ws, tuple) and len(ws) == 16 and all(isinstance(w, bool) for w in ws)
    ), "`ws` must be a 16-tuple of `bool`s"
    assert (
        isinstance(us, tuple) and len(us) == 16 and all(isinstance(u, bool) for u in us)
    ), "`us` must be a 16-tuple of `bool`s"
    assert (
        isinstance(vs, tuple) and len(vs) == 16 and all(isinstance(v, bool) for v in vs)
    ), "`vs` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ms, tuple) and len(ms) == 16 and all(isinstance(m, bool) for m in ms)
    ), "`ms` must be a 16-tuple of `bool`s"
    assert (
        isinstance(ns, tuple) and len(ns) == 16 and all(isinstance(n, bool) for n in ns)
    ), "`ns` must be a 16-tuple of `bool`s"
    assert (
        isinstance(sel, tuple)
        and len(sel) == 3
        and all(isinstance(s, bool) for s in sel)
    ), "`sel` must be a 3-tuple of `bool`s"

    # implementation
    out = MUX16(
        MUX4WAY16(xs, ys, zs, ws, sel=(sel[1], sel[2])),
        MUX4WAY16(us, vs, ms, ns, sel=(sel[1], sel[2])),
        sel[0],
    )

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 16
        and all(isinstance(o, bool) for o in out)
    ), "Output must be 16-tuple of `bool`s"

    return out


def DMUX4WAY(
    x: bool, sel: Tuple[bool]
) -> Tuple[Tuple[bool], Tuple[bool], Tuple[bool], Tuple[bool]]:
    """Channels the input to one out of four outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert (
        isinstance(sel, tuple)
        and len(sel) == 2
        and all(isinstance(s, bool) for s in sel)
    ), "`sel` must be a 2-tuple of `bool`s"

    # implementation
    x1, x2 = DMUX(x, sel[1])
    x3, x4 = DMUX(x, sel[1])
    out = (
        ((not sel[0]) and (not sel[1])) and x1,
        ((not sel[0]) and sel[1]) and x2,
        (sel[0] and (not sel[1])) and x3,
        (sel[0] and sel[1]) and x4,
    )

    # post-conditions
    assert (
        isinstance(out, tuple)
        and len(out) == 4
        and all(isinstance(x, bool) for x in out)
    ), "Output must be a 4-tuple of `bool`s"

    return out


def DMUX8WAY(
    xs: Tuple[bool], sel: Tuple[bool]
) -> Tuple[
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
    Tuple[bool],
]:
    """De-multiplexes a single input into eight outputs."""
    raise NotImplementedError()
