from pytest import param, mark
import adventure as ad


@mark.parametrize('data_file,expect', [
    param('example5.dat', 27730),
    param('example6.dat', 36334),
    param('example7.dat', 39514),
    param('example8.dat', 27755),
    param('example9.dat', 28944),
    param('example10.dat', 18740)
])
def test_solve_part1(data_file, expect):
    result = ad.solve_part1(data_file)
    assert result == expect


@mark.parametrize('data_file,expect', [
    param('example5.dat', 4988),
    param('example8.dat', 3478),
    param('example10.dat', 1140)
])
def test_solve_part2(data_file, expect):
    result = ad.solve_part2(data_file)
    assert result == expect
