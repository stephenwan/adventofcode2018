import adventure as ad


def test_solve_part1():
    result = ad.solve_part1('example1.dat')
    assert result == 7


def test_solve_part2():
    result = ad.solve_part2('example2.dat')
    assert result == 36
