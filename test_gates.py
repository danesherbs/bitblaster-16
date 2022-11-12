import gates

# elementary logic gates
def test_and():
    assert gates.AND(0, 0) == 0
    assert gates.AND(0, 1) == 0
    assert gates.AND(1, 0) == 0
    assert gates.AND(1, 1) == 1

def test_or():
    assert gates.OR(0, 0) == 0
    assert gates.OR(0, 1) == 1
    assert gates.OR(1, 0) == 1
    assert gates.OR(1, 1) == 1

def test_not():
    assert gates.NOT(0) == 1
    assert gates.NOT(1) == 0

def test_nand():
    assert gates.NAND(0, 0) == 1
    assert gates.NAND(0, 1) == 1
    assert gates.NAND(1, 0) == 1
    assert gates.NAND(1, 1) == 0

def test_xor():
    assert gates.XOR(0, 0) == 0
    assert gates.XOR(0, 1) == 1
    assert gates.XOR(1, 0) == 1
    assert gates.XOR(1, 1) == 0

def test_mux():
    raise NotImplementedError()

def test_dmux():
    raise NotImplementedError()

# 16-bit variants
def test_not16():
    raise NotImplementedError()

def test_and16():
    raise NotImplementedError()

def test_or16():
    raise NotImplementedError()

def test_mux16():
    raise NotImplementedError()

# multi-way variants
def test_or8way():
    raise NotImplementedError()

def test_mux4way16():
    raise NotImplementedError()

def test_mux8way16():
    raise NotImplementedError()

def test_dmux4way():
    raise NotImplementedError()

def test_dmux8way():
    raise NotImplementedError()
