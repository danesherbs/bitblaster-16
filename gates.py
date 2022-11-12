from typing import Tuple


# elementary logic gates
def AND(x: bool, y: bool) -> bool:
    """And gate."""
    return x and y

def OR(x: bool, y: bool) -> bool:
    """Or gate."""
    return x or y

def NOT(x: bool) -> bool:
    """Not gate."""
    return not x

def NAND(x: bool, y: bool) -> bool:
    """Nand gate."""
    return not(x and y)

def XOR(x: bool, y: bool) -> bool:
    """Xor gate."""
    return ((not x) and y) or (x and (not y))

def MUX(x: bool, y: bool, sel: bool) -> bool:
    """Selects between two inputs."""
    return (x and (not y) and (not sel)) or \
           (x and y and (not sel)) or \
           ((not x) and y and sel) or \
           (x and y and sel)

def DMUX(x: bool, sel: bool) -> Tuple[bool, bool]:
    """De-multiplexes a single input into two outputs."""
    return x and (not sel), x and sel


# 16-bit variants
def NOT16(xs: Tuple[bool]) -> Tuple[bool]:
    """16-bit Not."""
    assert len(xs) == 16
    return tuple(not x for x in xs)

def AND16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    """16-bit And."""
    assert len(xs) == 16 and len(ys) == 16
    return tuple(x and y for x, y in zip(xs, ys))

def OR16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    """16-bit Or."""
    assert len(xs) == 16 and len(ys) == 16
    return tuple(x or y for x, y in zip(xs, ys))

def MUX16(xs: Tuple[bool], ys: Tuple[bool], sel: bool) -> Tuple[bool]:
    """Selects between two 16-bit inputs."""
    assert len(xs) == 16 and len(ys) == 16
    return tuple(MUX(x, y, sel) for x, y in zip(xs, ys))

# multi-way variants
# TODO: Add stubs
