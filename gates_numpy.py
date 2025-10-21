import numpy as np
from numpy.typing import NDArray


def _is_n_bit_array(arr: NDArray[np.bool_], n: int) -> bool:
    """Check if arr is a numpy array of n boolean values."""
    return isinstance(arr, np.ndarray) and arr.dtype == bool and arr.shape == (n,)


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


def DMUX(x: bool, sel: bool) -> NDArray[np.bool_]:
    """Channels the input to one out of two outputs."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body
    out = np.array([x and (not sel), x and sel], dtype=bool)

    # post-conditions
    assert _is_n_bit_array(out, n=2), "Output must be numpy array of 2 bools"

    return out


# 16-bit variants (numpy-optimized)
def NOT16(xs: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """16-bit Not (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"

    # body - use numpy for vectorized operations
    out = ~xs

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


def AND16(xs: NDArray[np.bool_], ys: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """16-bit And (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ys, n=16), "`ys` must be numpy array of 16 bools"

    # body - use numpy for vectorized operations
    out = xs & ys

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


def OR16(xs: NDArray[np.bool_], ys: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """16-bit Or (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ys, n=16), "`ys` must be numpy array of 16 bools"

    # body - use numpy for vectorized operations
    out = xs | ys

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


def MUX16(xs: NDArray[np.bool_], ys: NDArray[np.bool_], sel: bool) -> NDArray[np.bool_]:
    """Selects between two 16-bit inputs (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ys, n=16), "`ys` must be numpy array of 16 bools"
    assert isinstance(sel, bool), "`sel` must be of type `bool`"

    # body - use numpy for vectorized operations
    # Use numpy's where function for conditional selection
    out = np.where(sel, ys, xs)

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


# multi-way variants (numpy-optimized)
def OR8WAY(xs: NDArray[np.bool_]) -> bool:
    """8-way Or (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=8), "`xs` must be numpy array of 8 bools"

    # body - use numpy's any function for efficient reduction
    out = bool(np.any(xs))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def OR16WAY(xs: NDArray[np.bool_]) -> bool:
    """16-way Or (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"

    # body - use numpy's any function for efficient reduction
    out = bool(np.any(xs))

    # post-conditions
    assert isinstance(out, bool), "Output must be of type `bool`"

    return out


def MUX4WAY16(
    xs: NDArray[np.bool_],
    ys: NDArray[np.bool_],
    zs: NDArray[np.bool_],
    ws: NDArray[np.bool_],
    sel: NDArray[np.bool_],
) -> NDArray[np.bool_]:
    """Selects between four 16-bit inputs (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ys, n=16), "`ys` must be numpy array of 16 bools"
    assert _is_n_bit_array(zs, n=16), "`zs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ws, n=16), "`ws` must be numpy array of 16 bools"
    assert _is_n_bit_array(sel, n=2), "`sel` must be numpy array of 2 bools"

    # body - use numpy for vectorized operations
    # sel = [sel[0], sel[1]]
    # 00 -> xs, 01 -> ys, 10 -> zs, 11 -> ws
    if not sel[0] and not sel[1]:
        out = xs
    elif not sel[0] and sel[1]:
        out = ys
    elif sel[0] and not sel[1]:
        out = zs
    else:  # sel[0] and sel[1]
        out = ws

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


def MUX8WAY16(
    xs: NDArray[np.bool_],
    ys: NDArray[np.bool_],
    zs: NDArray[np.bool_],
    ws: NDArray[np.bool_],
    us: NDArray[np.bool_],
    vs: NDArray[np.bool_],
    ms: NDArray[np.bool_],
    ns: NDArray[np.bool_],
    sel: NDArray[np.bool_],
) -> NDArray[np.bool_]:
    """Selects between eight 16-bit inputs (numpy-optimized)."""
    # pre-conditions
    assert _is_n_bit_array(xs, n=16), "`xs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ys, n=16), "`ys` must be numpy array of 16 bools"
    assert _is_n_bit_array(zs, n=16), "`zs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ws, n=16), "`ws` must be numpy array of 16 bools"
    assert _is_n_bit_array(us, n=16), "`us` must be numpy array of 16 bools"
    assert _is_n_bit_array(vs, n=16), "`vs` must be numpy array of 16 bools"
    assert _is_n_bit_array(ms, n=16), "`ms` must be numpy array of 16 bools"
    assert _is_n_bit_array(ns, n=16), "`ns` must be numpy array of 16 bools"
    assert _is_n_bit_array(sel, n=3), "`sel` must be numpy array of 3 bools"

    # body - use numpy for vectorized operations
    # sel = [sel[0], sel[1], sel[2]]
    # 000 -> xs, 001 -> ys, 010 -> zs, 011 -> ws
    # 100 -> us, 101 -> vs, 110 -> ms, 111 -> ns
    if not sel[0] and not sel[1] and not sel[2]:
        out = xs
    elif not sel[0] and not sel[1] and sel[2]:
        out = ys
    elif not sel[0] and sel[1] and not sel[2]:
        out = zs
    elif not sel[0] and sel[1] and sel[2]:
        out = ws
    elif sel[0] and not sel[1] and not sel[2]:
        out = us
    elif sel[0] and not sel[1] and sel[2]:
        out = vs
    elif sel[0] and sel[1] and not sel[2]:
        out = ms
    else:  # sel[0] and sel[1] and sel[2]
        out = ns

    # post-conditions
    assert _is_n_bit_array(out, n=16), "Output must be numpy array of 16 bools"

    return out


def DMUX4WAY(x: bool, sel: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """Channels the input to one out of four outputs (numpy-optimized)."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert _is_n_bit_array(sel, n=2), "`sel` must be numpy array of 2 bools"

    # body - use numpy for vectorized mask creation
    # Create output array with 4 positions
    out = np.zeros(4, dtype=bool)

    # Calculate which output position should be True
    if not sel[0] and not sel[1]:
        out[0] = x
    elif not sel[0] and sel[1]:
        out[1] = x
    elif sel[0] and not sel[1]:
        out[2] = x
    else:  # sel[0] and sel[1]
        out[3] = x

    # post-conditions
    assert _is_n_bit_array(out, n=4), "Output must be numpy array of 4 bools"

    return out


def DMUX8WAY(x: bool, sel: NDArray[np.bool_]) -> NDArray[np.bool_]:
    """Channels the input to one out of eight outputs (numpy-optimized)."""
    # pre-conditions
    assert isinstance(x, bool), "`x` must be of type `bool`"
    assert _is_n_bit_array(sel, n=3), "`sel` must be numpy array of 3 bools"

    # body - use numpy for vectorized mask creation
    # Create output array with 8 positions
    out = np.zeros(8, dtype=bool)

    # Calculate which output position should be True
    if not sel[0] and not sel[1] and not sel[2]:
        out[0] = x
    elif not sel[0] and not sel[1] and sel[2]:
        out[1] = x
    elif not sel[0] and sel[1] and not sel[2]:
        out[2] = x
    elif not sel[0] and sel[1] and sel[2]:
        out[3] = x
    elif sel[0] and not sel[1] and not sel[2]:
        out[4] = x
    elif sel[0] and not sel[1] and sel[2]:
        out[5] = x
    elif sel[0] and sel[1] and not sel[2]:
        out[6] = x
    else:  # sel[0] and sel[1] and sel[2]
        out[7] = x

    # post-conditions
    assert _is_n_bit_array(out, n=8), "Output must be numpy array of 8 bools"

    return out
