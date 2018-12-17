from pytest import param, mark
import adventure as ad


def test_generate_recipes():
    chain = ad.Chain()
    r1 = chain.add(3)
    r2 = chain.add(7)
    chain.generate_recipes(r1, r2)
    assert list(chain.scores()) == [3, 7, 1, 0]
    chain.generate_recipes(r1, r2)
    assert list(chain.scores()) == [3, 7, 1, 0, 1, 0]


def test_chain():
    chain = ad.Chain()
    for i in range(10):
        chain.add(i)
    assert list(chain.scores()) == list(range(10))
    r3 = chain.reciepe_at(3)
    assert r3.score == 3
    r7 = chain.recipe_at(4, start=r3)
    assert r7.score == 7
    rx = chain.recipe_at(10, start=r7)
    assert rx == r7


@mark.parametrize('input,expect', [
    param(9, '5158916779'),
    param(5, '0124515891'),
    param(18, '9251071085'),
    param(2018, '5941429882')
])
def test_solve_part1(input, expect):
    result = ad.solve_part1(input)
    assert result == expect


@mark.parametrize('input,expect', [
    param('5158916779', 9),
    param('01245', 5),
    param('92510', 18),
    param('59414', 2018),
    param('919901', 20203532)
])
def test_solve_part2(input, expect):
    result = ad.solve_part2(input)
    assert result == expect
