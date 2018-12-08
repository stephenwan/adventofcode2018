from pytest import param, mark
from adventure import P, Move, Op, Board
import adventure as ad


@mark.parametrize('pp,expect', [
    param((P(0, 1), P(1, 1)), {Move(1, 0), Move(0, 1), Move(0, -1)}),
    param((P(-1, 0), P(0, 1)), {Move(1, 0), Move(0, 1)}),
    param((P(100, -100), P(0, 0)), {Move(-1, 0), Move(0, 1)}),
    param((P(1, 1), P(1, 1)), {Move(-1, 0), Move(1, 0), Move(0, -1), Move(0, 1)})
])
def test_op(pp, expect):
    result = Op.get_moves(*pp)
    assert result == expect


@mark.parametrize('b,c,p,expect', [
    param(Board(4, 4), {P(2, 2)}, P(2, 2), {P(1, 2), P(2, 1), P(2, 3), P(3, 2)}),
    param(Board(4, 4), {P(0, 0)}, P(0, 0), {P(0, 1), P(1, 0)}),
    param(Board(4, 4), {P(3, 3)}, P(3, 3), {P(3, 2), P(2, 3)}),
    param(Board(4, 4), {P(0, 2)}, P(0, 2), {P(0, 1), P(0, 3), P(1, 2)}),
    param(Board(5, 5), {P(1, 3), P(1, 1)}, P(1, 2),
          {P(1, 0), P(1, 4), P(2, 1), P(2, 3), P(0, 1), P(0, 3)}),
    param(Board(5, 5), {P(2, 1), P(2, 3), P(1, 2), P(3, 2)}, P(2, 2),
          {P(2, 4), P(3, 3), P(4, 2), P(3, 1), P(2, 0), P(1, 1),
           P(0, 2), P(1, 3)})
])
def test_board_expand_contour_empty_board(b, c, p, expect):
    result = b.expand_contour(c, p)
    assert result == expect


def test_board_set_owner():
    board = Board(2, 2)
    board.set_owner(P(1, 1), 1)
    board.set_owner(P(1, 1), 2)
    assert board.get_owner(P(1, 1)) == -1
    board.set_owner(P(0, 1), 1)
    board.set_owner(P(0, 1), 1)
    assert board.get_owner(P(0, 1)) == 1
    assert board.get_owner(P(0, 0)) is None


def test_board_stats():
    board = Board(3, 3)
    board.set_owner(P(0, 1), 2)
    board.set_owner(P(1, 1), 1)
    stats = board.owner_stats()
    assert set(stats.items()) == {(2, 1), (1, 1)}


def test_solve_part1():
    raw_input = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''
    input = list(ad.parse_line(line) for line in raw_input.split('\n'))
    result = ad.solve_part1(input, 10)
    assert result == 17


def test_solve_part2():
    raw_input = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''
    input = list(ad.parse_line(line) for line in raw_input.split('\n'))
    result = ad.solve_part2(input, 10, 32)
    assert result == 16
