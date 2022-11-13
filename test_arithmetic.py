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
