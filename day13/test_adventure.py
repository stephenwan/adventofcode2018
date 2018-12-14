import adventure as ad
from lib.util import get_input_from_file


def test_solve_part1():
    example = get_input_from_file('example.dat', break_lines=False)
    tick, x, y = ad.solve_part1(example)
    assert (x, y) == (7, 3)


def test_solve_part2():
    example = get_input_from_file('example2.dat', break_lines=False)
    tick, x, y = ad.solve_part2(example)
    assert (x, y) == (6, 4)
