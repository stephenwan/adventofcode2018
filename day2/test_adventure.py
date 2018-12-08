from pytest import param, mark
from adventure import _part1_process_line, solve_part1, solve_part2


@mark.parametrize('line,expect', [
    param('abcdef', set()),
    param('bababc', {2, 3}),
    param('abbcde', {2}),
    param('abcccd', {3}),
    param('aabcdd', {2}),
    param('abcdee', {2}),
    param('ababab', {3})
])
def test_part1_process_line(line, expect):
    result = _part1_process_line(line)
    assert result == expect


@mark.parametrize('input,expect', [
    param(['abba', 'abbba'], 2),
    param(['abcd', 'efgh'], 1),
    param(['aaabb', 'ccddd'], 4)
])
def test_part1(input, expect):
    result = solve_part1(input)
    assert result == expect


@mark.parametrize('input,expect', [
    param(['abcdef', 'abddef'], 'abdef'),
    param(['abcdefg', 'bacdegf', 'bcdefgh'], 'bcdefg')
])
def test_part2(input, expect):
    result = solve_part2(input)
    assert result == expect
