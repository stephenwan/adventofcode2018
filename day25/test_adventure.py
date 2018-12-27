from pytest import param, mark
import adventure as ad


@mark.parametrize('input,expect', [
    param('example1.dat', 4),
    param('example2.dat', 3),
    param('example3.dat', 8),
])
def test_1(input, expect):
    result = ad.solve_part1(input)
    assert result == expect
