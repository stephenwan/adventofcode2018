from enum import Enum


class Direction(tuple, Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)

    @staticmethod
    def reading_order():
        return [Direction.N, Direction.W, Direction.E, Direction.S]

    @staticmethod
    def clock_order():
        return [Direction.N, Direction.E, Direction.S, Direction.W]

    def left(self):
        idx = Direction.clockwise().index(self)
        return Direction.clockwise[(idx - 1) % 4]

    def right(self):
        idx = Direction.clockwise().index(self)
        return Direction.clockwise[(idx + 1) % 4]

    def opposite(self):
        idx = Direction.clockwise().index(self)
        return Direction.clockwise[(idx + 2) % 4]


class Point():
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def neighbour(self, direction: Direction):
        if direction is None:
            return Point(self.y, self.x)
        dy, dx = direction.value
        return Point(self.y + dy, self.x + dx)

    def neighbours(self, order='clock_order'):
        if order == 'reading_order':
            return [self.neighbour(d) for d in Direction.reading_order()]
        else:
            return [self.neighbour(d) for d in Direction.clock_order()]

    @property
    def here(self):
        return self.neighbour()

    @property
    def north(self):
        return self.neighbour(Direction.N)

    @property
    def south(self):
        return self.neighbour(Direction.S)

    @property
    def east(self):
        return self.neighbour(Direction.E)

    @property
    def west(self):
        return self.neighbour(Direction.W)

    def distance(self, other):
        return abs(other.y - self.y) + abs(other.x - self.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __str__(self):
        return f'P{(self.y, self.x)}'

    def __repr__(self):
        return self.__str__()
