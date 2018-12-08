import adventure as ad


def test_parse_line():
    line = '#1 @ 1,3: 4x4'
    result = ad.parse_line(line)
    assert result == ad.Claim(1, 3, 5, 7, 1)


def test_segmentation():
    input = [
        ad.Claim(1, 2, 4, 3, 1),
        ad.Claim(2, 3, 5, 4, 2),
        ad.Claim(3, 4, 6, 5, 3)
    ]

    result = ad.segmentation(input, 'x')
    expect = [
        ad.Segment(1, 2, {1}),
        ad.Segment(2, 3, {1, 2}),
        ad.Segment(3, 4, {1, 2, 3}),
        ad.Segment(4, 5, {2, 3}),
        ad.Segment(5, 6, {3})
    ]
    assert result == expect

    result = ad.segmentation(input, 'y')
    expect = [
        ad.Segment(2, 3, {1}),
        ad.Segment(3, 4, {2}),
        ad.Segment(4, 5, {3})
    ]
    assert result == expect


def test_solve_part1_variant1():
    lines = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2'
    ]
    input = list(map(ad.parse_line, lines))
    print(f'input {input}')
    result = ad.solve_part1(input)
    assert result == 4


def test_solve_part1_variant2():
    lines = [
        '#1 @ 1,3: 4x4',
        '#2 @ 1,3: 4x4',
        '#3 @ 1,3: 2x2'
    ]
    input = list(map(ad.parse_line, lines))
    print(f'input {input}')
    result = ad.solve_part1(input)
    assert result == 16


def test_solve_part2_variant1():
    lines = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2'
    ]
    input = list(map(ad.parse_line, lines))
    print(f'input {input}')
    result = ad.solve_part2(input)
    assert result == {3}


def test_solve_part2_variant2():
    lines = [
        '#1 @ 1,3: 4x4',
        '#2 @ 1,3: 4x4',
        '#3 @ 1,3: 2x2'
    ]
    input = list(map(ad.parse_line, lines))
    print(f'input {input}')
    result = ad.solve_part2(input)
    assert result == set()
