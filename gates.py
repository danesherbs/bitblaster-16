# elementary logic gates
def AND(x: bool, y: bool) -> bool:
    return x and y

def OR(x: bool, y: bool) -> bool:
    return x or y

def NOT(x: bool) -> bool:
    return not x

def NAND(x: bool, y: bool) -> bool:
    return NOT(AND(x, y))

def XOR(x: bool, y: bool) -> bool:
    return OR(
        AND(NOT(x), y),
        AND(x, NOT(y)),
    )

# 16-bit variants

# multi-way variants
