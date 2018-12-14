import math
import operator
from itertools import product
from collections import defaultdict


def calculate_fuel(x, y, serial):
    rack = x + 10
    return math.floor((rack * y + serial) * rack % 1000 / 100) - 5


class Grid():
    def __init__(self, serial, size):
        self.serial = serial
        self.size = size
        self.squares = defaultdict(int)
        self.max_square_size = None

    def init_fuel(self):
        r = self.square_idx_range(1)
        for x, y in product(r, r):
            self.squares[(x, y, 1)] = calculate_fuel(x, y, self.serial)
        self.max_square_size = 1

    def square_idx_range(self, square_size):
        return range(1, self.size - square_size + 2)

    def expand_squares(self):
        size = self.max_square_size + 1
        r = self.square_idx_range(size)
        new_squares = {}
        for x, y in product(r, r):
            value = (self.squares[(x, y, size - 1)]
                     + self.squares[(x + 1, y + 1, size - 1)]
                     + self.squares[(x + size - 1, y, 1)]
                     + self.squares[(x, y + size - 1, 1)]
                     - self.squares[(x + 1, y + 1, size - 2)])
            new_squares[(x, y, size)] = value
            self.squares[(x, y, size)] = value
        self.max_square_size = size
        print(f'square size {size} added {len(new_squares)} squares')
        return new_squares


def solve_part1(serial, size):
    g = Grid(serial, size)
    g.init_fuel()
    g.expand_squares()
    square3s = g.expand_squares()
    (x, y, _), v = max(square3s.items(), key=operator.itemgetter(1))
    return (x, y), v


def solve_part2(serial, size):
    g = Grid(serial, size)
    g.init_fuel()
    while g.max_square_size < size:
        g.expand_squares()
    (x, y, s), v = max(g.squares.items(), key=operator.itemgetter(1))
    return (x, y, s), v
