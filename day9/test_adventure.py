from pytest import param, mark
import adventure as ad


def test_solve_variant1():
    result = ad.solve(9, 25)
    assert result == 32


def test_solve_variant2():
    result = ad.solve(411, 71058)
    assert result == 424639
