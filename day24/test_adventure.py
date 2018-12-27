from pytest import mark, param
import adventure as ad


def test_solve_part1():
    result = ad.solve_part1('example.dat')
    assert result == 5216
