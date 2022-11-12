from typing import Tuple


# elementary logic gates
def AND(x: bool, y: bool) -> bool:
    return x and y

def OR(x: bool, y: bool) -> bool:
    return x or y

def NOT(x: bool) -> bool:
    return not x

def NAND(x: bool, y: bool) -> bool:
    return not(x and y)

def XOR(x: bool, y: bool) -> bool:
    return ((not x) and y) or (x and (not y))

def MUX(x: bool, y: bool, sel: bool) -> bool:
    return (x and (not y) and (not sel)) or \
           (x and y and (not sel)) or \
           ((not x) and y and sel) or \
           (x and y and sel)

def DMUX(x: bool, sel: bool) -> Tuple[bool, bool]:
    return x and (not sel), x and sel


# 16-bit variants
def NOT16(xs: Tuple[bool]) -> Tuple[bool]:
    assert len(xs) == 16
    return tuple(not x for x in xs)

def AND16(xs: Tuple[bool], ys: Tuple[bool]) -> Tuple[bool]:
    assert len(xs) == 16 and len(ys) == 16
    return tuple(x and y for x, y in zip(xs, ys))


# multi-way variants
# TODO: Add stubs
