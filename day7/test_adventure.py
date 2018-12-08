from pytest import param, mark
import adventure as ad


def test_solve_part1_varaint1():
    input = [
        ('A', 'B'),
        ('B', 'D'),
        ('D', 'C')
    ]
    result = ad.solve_part1(input)
    assert result == 'ABDC'


def test_solve_part1_varaint2():
    input = [
        ('A', 'B'),
        ('A', 'E'),
        ('E', 'D')
    ]
    result = ad.solve_part1(input)
    assert result == 'ABED'


def test_solve_part1_varaint3():
    raw = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''

    input = [ad.parse_line(line) for line in raw.split('\n')]
    result = ad.solve_part1(input)
    assert result == 'CABDFE'


def test_solve_part2():
    raw = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''

    input = [ad.parse_line(line) for line in raw.split('\n')]
    time, result = ad.solve_part2(input, 2, 0)
    print(f'time {time} result {result}')
    assert result == 'CABFDE'
    assert time == 15
