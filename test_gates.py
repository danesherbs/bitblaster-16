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
    for x in [True, False]:
        for y in [True, False]:
                assert gates.MUX(x, y, sel=True) == y
                assert gates.MUX(x, y, sel=False) == x

def test_dmux():
    for x in [True, False]:
        assert gates.DMUX(x, sel=False) == (x, False)
        assert gates.DMUX(x, sel=True) == (False, x)


# 16-bit variants
def test_not16():
    assert gates.NOT16((False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) == (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)
    assert gates.NOT16((True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    assert gates.NOT16((True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True)) == (False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False)
    assert gates.NOT16((True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, False)) == (False, False, False, False, True, False, False, False, False, False, False, False, False, True, True, True)

def test_and16():
    assert gates.AND16((False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False), (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) == (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    assert gates.AND16((True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True), (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)
    assert gates.AND16((True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True), (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True)
    assert gates.AND16((True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, False), (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, False)

def test_or16():
    assert gates.OR16((False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False), (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) == (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    assert gates.OR16((True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True), (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)
    assert gates.OR16((True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False), (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)) == (True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)
    assert gates.OR16((False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False), (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)) == (False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    assert gates.OR16((True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False), (True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False)) == (True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False)

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
