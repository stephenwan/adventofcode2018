from pytest import param, mark
import adventure as ad


@mark.parametrize('input,expect', [
    param('abAB', 4),
    param('abBA', 0),
    param('aA', 0),
    param('ABCDEFGgfedcba', 0),
    param('aaaaaaa', 7),
    param('cCcCcCc', 1),
    param('abcCdDeEBa', 2),
    param('zacCdDAAcCdDaZ', 0),
    param('dabAcCaCBAcCcaDA', 10)
])
def test_solve_part1(input, expect):
    result = ad.solve_part1(input)
    assert result == expect


def test_solve_part2():
    input = 'dabAcCaCBAcCcaDA'
    expect = 4
    result = ad.solve_part2(input)
    assert result == expect
