from pytest import param, mark
import adventure as ad
from datetime import datetime as dt


@mark.parametrize('line,expect', [
    param('[1518-11-22 00:49] wakes up',
          ad.Record(dt(1518, 11, 22, 0, 49), ad.Info(None, True))),
    param('[1518-05-18 00:01] Guard #1171 begins shift',
          ad.Record(dt(1518, 5, 18, 0, 1), ad.Info(1171, True))),
    param('[1518-09-09 00:16] falls asleep',
          ad.Record(dt(1518, 9, 9, 0, 16), ad.Info(None, False)))
])
def test_parse_line(line, expect):
    result = ad.parse_line(line)
    assert result == expect


def test_solve_part1_variant1():
    txt = '''[1518-10-20 23:55] Guard #10 begins shift
[1518-10-21 00:02] falls asleep
[1518-10-21 00:12] wakes up
[1518-10-21 23:55] Guard #10 begins shift
[1518-10-22 00:11] falls asleep
[1518-10-22 00:15] wakes up'''
    input = [ad.parse_line(line) for line in txt.split('\n')]
    result = ad.solve_part1(input)
    assert result == 110


def test_solve_part1_variant2():
    txt = '''[1518-10-20 23:55] Guard #10 begins shift
[1518-10-21 00:02] falls asleep
[1518-10-21 00:12] wakes up
[1518-10-23 23:55] Guard #13 begins shift
[1518-10-24 00:02] falls asleep
[1518-10-24 00:42] wakes up
[1518-10-21 23:55] Guard #10 begins shift
[1518-10-22 00:11] falls asleep
[1518-10-22 00:15] wakes up'''
    input = [ad.parse_line(line) for line in txt.split('\n')]
    result = ad.solve_part1(input)
    assert result == 26


def test_solve_part2():
    txt = '''[1518-10-20 23:55] Guard #10 begins shift
[1518-10-21 00:02] falls asleep
[1518-10-21 00:12] wakes up
[1518-10-23 23:55] Guard #13 begins shift
[1518-10-24 00:02] falls asleep
[1518-10-24 00:42] wakes up
[1518-10-21 23:55] Guard #10 begins shift
[1518-10-22 00:11] falls asleep
[1518-10-22 00:12] wakes up'''
    input = [ad.parse_line(line) for line in txt.split('\n')]
    result = ad.solve_part2(input)
    assert result == 110
