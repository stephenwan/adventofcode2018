import adventure as ad


def test_mulr():
    rs = [3, 2, 1, 1]
    ad.mulr(rs, 2, 1, 2)
    assert rs == [3, 2, 2, 1]


def test_eqir():
    rs = [0, 0, 0, 0]
    ad.eqir(rs, 3, 0, 0)
    assert rs == [0, 0, 0, 0]
