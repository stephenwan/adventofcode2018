from pytest import param, mark
import day11.adventure as ad


@mark.parametrize(('x,y,serial,expect'), [
    param(3, 5, 8, 4),
    param(122, 79, 57, -5),
    param(217, 196, 39, 0),
    param(101, 153, 71, 4)
])
def test_calculate_fuel(x, y, serial, expect):
    result = ad.calculate_fuel(x, y, serial)
    assert result == expect


@mark.parametrize(('serial,size,expect'), [
    param(18, 300, ((33, 45), 29)),
    param(42, 300, ((21, 61), 30))
])
def test_solve_part1(serial, size, expect):
    result = ad.solve_part1_np(serial, size)
    assert result == expect


@mark.parametrize(('serial,size,expect'), [
    param(18, 300, ((90, 269, 16), 113))
])
def test_solve_part2(serial, size, expect):
    result = ad.solve_part2(serial, size)
    assert result == expect
