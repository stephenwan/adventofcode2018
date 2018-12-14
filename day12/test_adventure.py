import adventure as ad


def test_solve_part1():
    pattern_str = '''...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''
    initial_str = '#..#.#..##......###...###'
    result = ad.solve_part1(pattern_str, initial_str)
    assert result == 325
