from collections import namedtuple, defaultdict
from itertools import islice, cycle, product

P = namedtuple('P', 'x,y')
Move = namedtuple('Move', 'x,y')


class Op():
    moves = {Move(1, 0), Move(0, 1), Move(-1, 0), Move(0, -1)}

    @staticmethod
    def get_moves(p_from, p_to):
        exclude_moves = set()
        if p_to.y != p_from.y:
            exclude_moves.add(Move(0, -1 if p_to.y > p_from.y else 1))
        if p_to.x != p_from.x:
            exclude_moves.add(Move(-1 if p_to.x > p_from.x else 1, 0))
        return Op.moves.difference(exclude_moves)

    @staticmethod
    def distance(p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)


class Board():
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.owner_details = []

        for y, x in product(range(size_y), range(size_x)):
            self.owner_details.append({
                'p': P(x, y),
                'owner': None
            })

    def p_valid(self, p):
        return p.x >= 0 and p.x < self.size_x and p.y >= 0 and p.y < self.size_y

    def get_owner(self, p):
        return self.owner_details[p.y * self.size_x + p.x]['owner']

    def has_owner(self, p):
        return self.get_owner(p) is not None

    def set_owner(self, p, owner):
        cur = self.owner_details[p.y * self.size_x + p.x]
        if cur['owner'] is None:
            cur['owner'] = owner
            return True
        elif cur['owner'] < 0 or cur['owner'] == owner:
            return False
        else:
            cur['owner'] = -1
            return False

    def mark_contour_owner(self, contour, owner):
        count_marked = 0
        for p in contour:
            marked = self.set_owner(p, owner)
            if marked:
                count_marked += 1
        return count_marked

    def expand_contour(self, contour, pivot):
        new_contour = set()
        for p in contour:
            for m in Op.get_moves(pivot, p):
                p_next = P(p.x + m.x, p.y + m.y)
                if self.p_valid(p_next) and not self.has_owner(p_next):
                    new_contour.add(p_next)
        return new_contour

    def owner_stats(self):
        stats = defaultdict(int)
        for detail in self.owner_details:
            if detail['owner'] is None or detail['owner'] < 0:
                continue
            stats[detail['owner']] = stats[detail['owner']] + 1
        return stats

    def boundary_owners(self):
        b_u = {self.get_owner(P(x, 0)) for x in range(self.size_x)}
        b_d = {self.get_owner(P(x, self.size_y - 1)) for x in range(self.size_x)}
        b_l = {self.get_owner(P(0, y)) for y in range(self.size_y)}
        b_r = {self.get_owner(P(self.size_x - 1, y)) for y in range(self.size_y)}
        return set().union(b_u).union(b_d).union(b_l).union(b_r)


def solve_part1(input, size):
    board = Board(size, size)
    contours = [{'pivot': p, 'owner': idx, 'contour': {p}}
                for idx, p in enumerate(input)]

    while True:
        total_marked = sum(board.mark_contour_owner(c['contour'], c['owner'])
                           for c in contours)
        print(f'total marked { total_marked }')
        for c in contours:
            c['contour'] = board.expand_contour(c['contour'], c['pivot'])

        total_contour_length = sum(len(c['contour']) for c in contours)
        if total_contour_length == 0:
            break

    boundary_owners = board.boundary_owners()
    stats = board.owner_stats()
    return max(c for o, c in stats.items() if o not in boundary_owners)


def solve_part2(input, size, threshold):
    count = 0
    for x, y in product(range(size), range(size)):
        total_distance = sum(Op.distance(P(x, y), pivot) for pivot in input)
        if total_distance < threshold:
            count += 1
    return count


def parse_line(line):
    x, y = line.split(',')
    return P(int(x.strip()), int(y.strip()))
