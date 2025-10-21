import numpy as np
from numpy.typing import NDArray
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


# 16-bit variants (numpy-optimized)
def NOT16(xs: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit Not (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    out_arr = ~xs_arr
    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def AND16(xs: tuple[bool, ...], ys: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit And (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    ys_arr = np.array(ys, dtype=bool)
    out_arr = xs_arr & ys_arr
    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def OR16(xs: tuple[bool, ...], ys: tuple[bool, ...]) -> tuple[bool, ...]:
    """16-bit Or (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    ys_arr = np.array(ys, dtype=bool)
    out_arr = xs_arr | ys_arr
    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def MUX16(xs: tuple[bool, ...], ys: tuple[bool, ...], sel: bool) -> tuple[bool, ...]:
    """Selects between two 16-bit inputs (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be 16-tuple of `bool`s"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    ys_arr = np.array(ys, dtype=bool)
    # Use numpy's where function for conditional selection
    out_arr = np.where(sel, ys_arr, xs_arr)
    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


# multi-way variants (numpy-optimized)
def OR8WAY(xs: tuple[bool, ...]) -> bool:
    """8-way Or (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=8), "`xs` must be an 8-tuple of `bool`s"

    # body - use numpy's any function for efficient reduction
    xs_arr = np.array(xs, dtype=bool)
    out = bool(np.any(xs_arr))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def OR16WAY(xs: tuple[bool, ...]) -> bool:
    """16-way Or (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be an 16-tuple of `bool`s"

    # body - use numpy's any function for efficient reduction
    xs_arr = np.array(xs, dtype=bool)
    out = bool(np.any(xs_arr))

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
    """Selects between four 16-bit inputs (numpy-optimized)."""
    # pre-conditions
    assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ys, n=16), "`ys` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(zs, n=16), "`zs` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(ws, n=16), "`ws` must be a 16-tuple of `bool`s"
    assert is_n_bit_vector(sel, n=2), "`sel` must be a 2-tuple of `bool`s"

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    ys_arr = np.array(ys, dtype=bool)
    zs_arr = np.array(zs, dtype=bool)
    ws_arr = np.array(ws, dtype=bool)

    # Create selection logic using numpy
    # sel = [sel[0], sel[1]]
    # 00 -> xs, 01 -> ys, 10 -> zs, 11 -> ws
    if not sel[0] and not sel[1]:
        out_arr = xs_arr
    elif not sel[0] and sel[1]:
        out_arr = ys_arr
    elif sel[0] and not sel[1]:
        out_arr = zs_arr
    else:  # sel[0] and sel[1]
        out_arr = ws_arr

    out = tuple(bool(x) for x in out_arr)

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
    """Selects between eight 16-bit inputs (numpy-optimized)."""
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

    # body - use numpy for vectorized operations
    xs_arr = np.array(xs, dtype=bool)
    ys_arr = np.array(ys, dtype=bool)
    zs_arr = np.array(zs, dtype=bool)
    ws_arr = np.array(ws, dtype=bool)
    us_arr = np.array(us, dtype=bool)
    vs_arr = np.array(vs, dtype=bool)
    ms_arr = np.array(ms, dtype=bool)
    ns_arr = np.array(ns, dtype=bool)

    # Create selection logic using numpy
    # sel = [sel[0], sel[1], sel[2]]
    # 000 -> xs, 001 -> ys, 010 -> zs, 011 -> ws
    # 100 -> us, 101 -> vs, 110 -> ms, 111 -> ns
    if not sel[0] and not sel[1] and not sel[2]:
        out_arr = xs_arr
    elif not sel[0] and not sel[1] and sel[2]:
        out_arr = ys_arr
    elif not sel[0] and sel[1] and not sel[2]:
        out_arr = zs_arr
    elif not sel[0] and sel[1] and sel[2]:
        out_arr = ws_arr
    elif sel[0] and not sel[1] and not sel[2]:
        out_arr = us_arr
    elif sel[0] and not sel[1] and sel[2]:
        out_arr = vs_arr
    elif sel[0] and sel[1] and not sel[2]:
        out_arr = ms_arr
    else:  # sel[0] and sel[1] and sel[2]
        out_arr = ns_arr

    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=16), "Output must be 16-tuple of `bool`s"

    return out


def DMUX4WAY(x: bool, sel: tuple[bool, ...]) -> tuple[bool, bool, bool, bool]:
    """Channels the input to one out of four outputs (numpy-optimized)."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert is_n_bit_vector(sel, n=2), "`sel` must be a 2-tuple of `bool`s"

    # body - use numpy for vectorized mask creation
    # Create output array with 4 positions
    out_arr = np.zeros(4, dtype=bool)

    # Calculate which output position should be True
    if not sel[0] and not sel[1]:
        out_arr[0] = x
    elif not sel[0] and sel[1]:
        out_arr[1] = x
    elif sel[0] and not sel[1]:
        out_arr[2] = x
    else:  # sel[0] and sel[1]
        out_arr[3] = x

    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=4), "Output must be a 4-tuple of `bool`s"

    return out


def DMUX8WAY(
    x: bool, sel: tuple[bool, ...]
) -> tuple[bool, bool, bool, bool, bool, bool, bool, bool]:
    """Channels the input to one out of eight outputs (numpy-optimized)."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert is_n_bit_vector(sel, n=3), "`sel` must be a 3-tuple of `bool`s"

    # body - use numpy for vectorized mask creation
    # Create output array with 8 positions
    out_arr = np.zeros(8, dtype=bool)

    # Calculate which output position should be True
    if not sel[0] and not sel[1] and not sel[2]:
        out_arr[0] = x
    elif not sel[0] and not sel[1] and sel[2]:
        out_arr[1] = x
    elif not sel[0] and sel[1] and not sel[2]:
        out_arr[2] = x
    elif not sel[0] and sel[1] and sel[2]:
        out_arr[3] = x
    elif sel[0] and not sel[1] and not sel[2]:
        out_arr[4] = x
    elif sel[0] and not sel[1] and sel[2]:
        out_arr[5] = x
    elif sel[0] and sel[1] and not sel[2]:
        out_arr[6] = x
    else:  # sel[0] and sel[1] and sel[2]
        out_arr[7] = x

    out = tuple(bool(x) for x in out_arr)

    # post-conditions
    assert is_n_bit_vector(out, n=8), "Output must be a 8-tuple of `bool`s"

    return out
