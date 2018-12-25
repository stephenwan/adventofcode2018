from pytest import mark, param
import adventure as ad
from lib.geo import Point


@mark.parametrize('input,expect', [
    param((0, 0), 510),
    param((0, 1), 17317),
    param((1, 1), 1805),
    param((10, 10), 510),
])
def test_erosion_level(input, expect):
    cave = ad.Cave(510, Point(10, 10))
    result = cave.erosion_lvl(Point(*input))
    assert result == expect


def test_total_risk_level():
    cave = ad.Cave(510, Point(10, 10))
    result = cave.total_risk_lvl()
    assert result == 114


def test_fastest_first_search():
    cave = ad.Cave(510, Point(10, 10))
    rescue = ad.Rescue(cave)
    cost = rescue.fastest_first_search(Point(0, 0), 1)
    print(f'cost {rescue.cost_cache}')
    assert cost == 45
