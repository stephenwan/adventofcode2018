from collections import defaultdict
from lib.alg import bfs


def from_file_data(file_path):
    from lib.util import get_input_from_file
    text = get_input_from_file(file_path, break_lines=False)
    return text


opposites = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}


def minmax(seq):
    return min(seq), max(seq)


class Point():
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def query(self, symbol):
        if symbol == 'N':
            return self.north
        elif symbol == 'S':
            return self.south
        elif symbol == 'E':
            return self.east
        elif symbol == 'W':
            return self.west
        else:
            return self.here

    @property
    def here(self):
        return Point(self.y, self.x)

    @property
    def north(self):
        return Point(self.y - 1, self.x)

    @property
    def south(self):
        return Point(self.y + 1, self.x)

    @property
    def east(self):
        return Point(self.y, self.x + 1)

    @property
    def west(self):
        return Point(self.y, self.x - 1)

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


class Construction:
    def __init__(self):
        self.rooms = defaultdict(set)

    def explore_one_step(self, p, s=None):
        n = p.query(s)
        if n != p:
            self.rooms[p].add(s)
            self.rooms[n].add(opposites[s])
        return n

    def explore_composite(self, ps, token_stream):
        new_ps = ps
        token = None
        while True:
            try:
                token = next(token_stream)
            except StopIteration:
                break
            if token in '^$':
                continue
            if token in 'NSWE':
                new_ps = set(self.explore_one_step(p, token) for p in new_ps)
            elif token == '(':
                new_ps, _ = self.explore_composite(new_ps, token_stream)
            elif token == ')':
                break
            elif token == '|':
                alternative_ps, last_token = self.explore_composite(ps, token_stream)
                new_ps = new_ps.union(alternative_ps)
                if last_token == ')':
                    token = ')'
                    break
            else:
                break
        return new_ps, token

    @property
    def vrange(self):
        return minmax([k.y for k in self.rooms.keys()])

    @property
    def hrange(self):
        return minmax([k.x for k in self.rooms.keys()])

    def __str__(self):
        min_y, max_y = self.vrange
        min_x, max_x = self.hrange

        n_rows = (max_y - min_y + 1) * 2 + 1
        n_cols = (max_x - min_x + 1) * 2 + 1
        pixels = [[' ' for _ in range(n_cols)] for _ in range(n_rows)]

        for j in range(0, n_rows, 2):
            for i in range(0, n_cols, 2):
                pixels[j][i] = '#'
            for i in range(1, n_cols, 2):
                if j == 0 or j == n_rows - 1:
                    pixels[j][i] = '#'
                else:
                    pixels[j][i] = '?'

        for j in range(1, n_rows, 2):
            for i in range(0, n_cols, 2):
                if i == 0 or i == n_cols - 1:
                    pixels[j][i] = '#'
                else:
                    pixels[j][i] = '?'

        for y in range(max_y - min_y + 1):
            for x in range(max_x - min_x + 1):
                p = Point(min_y + y, min_x + x)
                if p not in self.rooms:
                    continue
                if 'N' in self.rooms[p]:
                    pixels[2 * y][2 * x + 1] = '-'
                if 'S' in self.rooms[p]:
                    pixels[2 * y + 2][2 * x + 1] = '-'
                if 'E' in self.rooms[p]:
                    pixels[2 * y + 1][2 * x + 2] = '|'
                if 'W' in self.rooms[p]:
                    pixels[2 * y + 1][2 * x] = '|'

        for j in range(n_rows):
            for i in range(n_cols):
                if pixels[j][i] == '?':
                    pixels[j][i] = '#'

        pixels[2 * (0 - min_y) + 1][2 * (0 - min_x) + 1] = 'o'
        return '\n'.join([''.join(pixels[j])
                          for j in range(n_rows)])


def solve_part1(text):
    con = Construction()
    con.explore_composite({Point(0, 0)}, iter(text))
    print(f'{con}')

    def lookup_children(node):
        return [node.query(s) for s in con.rooms[node]]

    furthest_path = bfs(Point(0, 0),
                        lookup_children=lookup_children, with_distance=True)
    return furthest_path[-1]['node'], furthest_path[-1]['distance']


def solve_part2(text, threshold):
    con = Construction()
    con.explore_composite({Point(0, 0)}, iter(text))
    print(f'{con}')
    print(f'{con.vrange} {con.hrange}')

    lt_threshold = set()
    ge_threshold = set()

    def lookup_children(node):
        return [node.query(s) for s in con.rooms[node]]

    def on_node_begin(node, distance):
        if distance < threshold:
            lt_threshold.add(node)
        else:
            ge_threshold.add(node)
        return True

    bfs(Point(0, 0), on_node_begin=on_node_begin,
        lookup_children=lookup_children, with_distance=True)
    return len(lt_threshold), len(ge_threshold),
