import pytest
from adventure import solve_part2


def _decode_test_input(line):
    return [int(t) for t in line.split(', ')]


@pytest.mark.parametrize('line,expect', [
    pytest.param('+1, -1', 0),
    pytest.param('+3, +3, +4, -2, -4', 10),
    pytest.param('-6, +3, +8, +5, -6', 5),
    pytest.param('+7, +7, -2, -7, -4', 14)
])
def test_solve_part2(line, expect):
    result = solve_part2(_decode_test_input(line))
    assert result == expect
