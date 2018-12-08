from pytest import param, mark
import adventure as ad


def test_solve_part1():
    raw = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    input = ad.parse_line(raw)
    meta_sum = ad.solve_part1(input)
    assert meta_sum == 138


def test_solve_part2():
    raw = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    input = ad.parse_line(raw)
    value = ad.solve_part2(input)
    assert value == 66
