import arithmetic


def test_halfadder():
    assert arithmetic.HALFADDER(False, False) == (False, False)
    assert arithmetic.HALFADDER(False, True) == (True, False)
    assert arithmetic.HALFADDER(True, False) == (True, False)
    assert arithmetic.HALFADDER(True, True) == (True, True)


def test_fulladder():
    assert arithmetic.FULLADDER(False, False, False) == (False, False)
    assert arithmetic.FULLADDER(False, False, True) == (True, False)
    assert arithmetic.FULLADDER(False, True, False) == (True, False)
    assert arithmetic.FULLADDER(False, True, True) == (False, True)
    assert arithmetic.FULLADDER(True, False, False) == (True, False)
    assert arithmetic.FULLADDER(True, False, True) == (False, True)
    assert arithmetic.FULLADDER(True, True, False) == (False, True)
    assert arithmetic.FULLADDER(True, True, True) == (True, True)


def test_add16():
    assert arithmetic.ADD16((False,) * 16, (False,) * 16) == (False,) * 16
    assert arithmetic.ADD16((False,) * 16, (True,) * 16) == (True,) * 16
    assert arithmetic.ADD16((True,) * 16, (False,) * 16) == (True,) * 16
    assert arithmetic.ADD16((True,) * 16, (False,) * 15 + (True,)) == (False,) * 16


def test_inc16():
    assert arithmetic.INC16((False,) * 16) == (False,) * 15 + (True,)
    assert arithmetic.INC16((True,) * 16) == (False,) * 16


def test_neg16():
    assert arithmetic.NEG16((False,) * 16) == (False,) * 16
    assert arithmetic.NEG16((True,) * 16) == (False,) * 15 + (True,)


def test_alu():
    pass
