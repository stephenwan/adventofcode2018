import pytest
import day17.adventure as ad
import lib.util as u


@pytest.fixture
def text_input_1():
    return '\n'.join([
        'y=0, x=0..1',
        'y=10, x=0..10',
        'x=2, y=3..10',
        'x=8, y=7..10'
    ])


@pytest.fixture
def text_input_2():
    return '\n'.join([
        'y=0, x=0..1',
        'y=10, x=0..10',
        'x=2, y=3..10',
        'x=8, y=3..10'
    ])


def test_parse_line():
    line = 'x=529, y=1498..1500'
    result = ad.parse_line(line)
    assert result == [(1498, 529), (1499, 529), (1500, 529)]


def test_water_drop(text_input_1):
    ground, _ = ad.from_text_data(text_input_1)
    driplet = ad.Water(4, 8, False)
    ground.driplets.add(driplet)
    ground.squares[4, 8] = driplet
    print(ground)
    ground.water_drop(driplet)
    print(ground)
    assert ground.driplets == {ad.Water(6, 8, False),
                               ad.Water(1, 500, False)}


def test_water_sink(text_input_1):
    ground, _ = ad.from_text_data(text_input_1)
    for y in range(10):
        ground.squares[y, 5] = ad.Water(y, 5, False)
    driplet = ground.squares[9, 5]
    ground.driplets.add(driplet)
    print(ground)
    ground.water_sink(driplet)
    print(ground)
    assert ground.driplets == {ad.Water(6, 5, False),
                               ad.Water(1, 500, False)}


def test_water_sink_2(text_input_2):
    ground, _ = ad.from_text_data(text_input_2)
    for y in range(10):
        ground.squares[y, 5] = ad.Water(y, 5, False)
    driplet = ground.squares[9, 5]
    ground.driplets.add(driplet)
    print(ground)
    ground.water_sink(driplet)
    print(ground)
    assert ground.driplets == {ad.Water(2, 5, False),
                               ad.Water(1, 500, False)}


def test_water_splash(text_input_1):
    ground, _ = ad.from_text_data(text_input_1)
    for y in range(10):
        ground.squares[y, 5] = ad.Water(y, 5, False)
    driplet = ground.squares[9, 5]
    ground.driplets.add(driplet)
    print(ground)
    ground.water_sink(driplet)
    print(ground)
    ground.water_splash(next(iter(ground.driplets)))
    print(ground)
    assert ground.driplets == {ad.Water(6, 9, False),
                               ad.Water(1, 500, False)}


def test_water_splash2(text_input_2):
    ground, _ = ad.from_text_data(text_input_2)
    for y in range(10):
        ground.squares[y, 5] = ad.Water(y, 5, False)
    driplet = ground.squares[9, 5]
    ground.driplets.add(driplet)
    print(ground)
    ground.water_sink(driplet)
    print(ground)
    ground.water_splash(next(iter(ground.driplets)))
    print(ground)
    assert ground.driplets == {ad.Water(2, 1, False),
                               ad.Water(2, 9, False),
                               ad.Water(1, 500, False)}



def test_solve_parts_example():
    text = u.get_input_from_file('example.dat', break_lines=False)
    result = ad.solve_part_1_and_2(text)
    assert result == (57, 29)
