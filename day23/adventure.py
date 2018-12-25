import numpy as np
import pandas as pd
from queue import PriorityQueue, Empty
from itertools import product
import math


def mah_d(p1, p2):
    return np.abs(p1['x'] - p2['x']) \
        + np.abs(p1['y'] - p2['y']) \
        + np.abs(p1['z'] - p2['z'])


def wrap_xyz(x, y, z):
    return {'x': x, 'y': y, 'z': z}


class Bots:
    def __init__(self, records):
        self.df = pd.DataFrame.from_records(records, columns=['x', 'y', 'z', 'r'])

    def distance(self, x, y, z):
        return mah_d(self.df, wrap_xyz(x, y, z))

    def get_bot(self, idx):
        return tuple(self.df.iloc[idx])

    def count_in_range(self, block):
        distance = pd.Series(np.zeros(len(self.df)))
        for rg, ps in zip((block.xr, block.yr, block.zr),
                          (self.df.x, self.df.y, self.df.z)):
            lo, hi = rg
            distance += np.where(ps > hi, ps - hi, 0)
            distance += np.where(ps < lo, lo - ps, 0)

        return sum(distance <= self.df.r)

    def get_bounding_block(self):
        x_range = (np.min(self.df['x'] - self.df['r']),
                   np.max(self.df['x'] + self.df['r']))
        y_range = (np.min(self.df['y'] - self.df['r']),
                   np.max(self.df['y'] + self.df['r']))
        z_range = (np.min(self.df['z'] - self.df['r']),
                   np.max(self.df['z'] + self.df['r']))
        return Block(x_range, y_range, z_range)


class Block:
    def __init__(self, x_range, y_range, z_range):
        self.xr = x_range
        self.yr = y_range
        self.zr = z_range

    def split(self):
        def divide_range(lo, hi):
            if lo == hi:
                return [(lo, hi)]
            mid = math.floor((hi + lo) / 2)
            return [(lo, mid), (mid + 1, hi)]

        sub_ranges = [divide_range(lo, hi) for lo, hi
                      in (self.xr, self.yr, self.zr)]

        return [Block(*rs) for rs in product(*sub_ranges)]

    def size(self):
        return max((hi - lo + 1) for lo, hi
                   in (self.xr, self.yr, self.zr))

    @property
    def center(self):
        return int(np.mean(self.xr)), int(np.mean(self.yr)), int(np.mean(self.zr))

    def from_origin(self):
        return mah_d(wrap_xyz(0, 0, 0), wrap_xyz(*self.center))

    def __str__(self):
        return f'Block({self.xr, self.yr, self.zr})'

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return (self.xr, self.yr, self.zr) < (other.xr, other.yr, other.zr)


def solve_part1(file_path):
    records = from_file_data(file_path)
    bots = Bots(records)

    idx = bots.df.r.idxmax()
    x, y, z, r = bots.get_bot(idx)
    return sum(bots.distance(x, y, z) <= r)


def solve_part2(file_path):
    records = from_file_data(file_path)
    bots = Bots(records)

    initial_block = bots.get_bounding_block()
    print(f'initial_block {initial_block}')

    def calc_score(block):
        return (-bots.count_in_range(block),
                block.from_origin(),
                block.size())

    queue = PriorityQueue()
    queue.put((calc_score(initial_block), initial_block))

    lowest_score = None
    lowest_point = None

    while True:
        try:
            score, block = queue.get_nowait()
        except Empty:
            break

        if lowest_score is not None and score[0] > lowest_score[0]:
            continue

        if block.size() == 1:
            if lowest_score is None or score < lowest_score:
                lowest_score = score
                lowest_point = block.center
            continue

        for child in block.split():
            s = calc_score(child)
            queue.put((s, child))

    print(f'lowest_score: {lowest_score} lowest_point: {lowest_point}')
    return lowest_score[1]


def from_file_data(file_path):
    from lib.util import get_input_from_file
    import re

    def parse_line(line):
        pattern = r'pos=<(?P<x>[\d-]+),(?P<y>[\d-]+),(?P<z>[\d-]+)>, r=(?P<r>\d+)'
        match = re.match(pattern, line)
        return (int(match.group('x')),
                int(match.group('y')),
                int(match.group('z')),
                int(match.group('r')))

    return get_input_from_file(file_path, break_lines=True, parser=parse_line)
