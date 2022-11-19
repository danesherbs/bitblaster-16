import arithmetic


def test_halfadder():
    arithmetic.HALFADDER(False, False) == (False, False)
    arithmetic.HALFADDER(False, True) == (True, False)
    arithmetic.HALFADDER(True, False) == (True, False)
    arithmetic.HALFADDER(True, True) == (True, True)


def test_fulladder():
    arithmetic.FULLADDER(False, False, False) == (False, False)
    arithmetic.FULLADDER(False, False, True) == (True, False)
    arithmetic.FULLADDER(False, True, False) == (True, False)
    arithmetic.FULLADDER(False, True, True) == (False, True)
    arithmetic.FULLADDER(True, False, False) == (True, False)
    arithmetic.FULLADDER(True, False, True) == (False, True)
    arithmetic.FULLADDER(True, True, False) == (False, True)
    arithmetic.FULLADDER(True, True, True) == (True, True)


def test_add16():
    arithmetic.ADD16((False,) * 16, (False,) * 16) == (False,) * 16
    arithmetic.ADD16((False,) * 16, (True,) * 16) == (True,) * 16
    arithmetic.ADD16((True,) * 16, (False,) * 16) == (True,) * 16
    arithmetic.ADD16((True,) * 16, (False,) * 15 + (True,)) == (False,) * 16


def test_inc16():
    arithmetic.INC16((False,) * 16) == (False,) * 15 + (True,)
    arithmetic.INC16((True,) * 16) == (False,) * 16
