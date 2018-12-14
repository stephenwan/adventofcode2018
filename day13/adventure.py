from collections import namedtuple, defaultdict
from itertools import product


def solve_part1(input):
    grid, carts = from_grid_text(input)
    tick = 0
    cart_locations = set((c.x, c.y) for c in carts)
    while True:
        tick += 1
        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            cart_locations.remove((cart.x, cart.y))
            cart.move(grid)
            if (cart.x, cart.y) in cart_locations:
                return tick, cart.x, cart.y
            cart_locations.add((cart.x, cart.y))
        print(f'Tick {tick} \n')
        # grid.show(carts)


def solve_part2(input):
    grid, carts = from_grid_text(input)
    tick = 0
    cart_locations = set((c.x, c.y) for c in carts)
    while True:
        tick += 1
        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            if cart.dead:
                continue
            cart_locations.remove((cart.x, cart.y))
            cart.move(grid)
            if (cart.x, cart.y) in cart_locations:
                cart_locations.remove((cart.x, cart.y))
                for c in carts:
                    if (c.x, c.y) == (cart.x, cart.y):
                        c.dead = True
            else:
                cart_locations.add((cart.x, cart.y))
        carts = [c for c in carts if not c.dead]
        print(f'Tick {tick} remaining carts {len(carts)}\n')
        # grid.show(carts)
        if len(carts) == 1:
            return tick, carts[0].x, carts[0].y


Site = namedtuple('Site', 'x,y,connections')


class Op:
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)
    North = (0, -1)
    Directions = [East, South, West, North]

    @staticmethod
    def opposite(direction):
        return Op.Directions[(Op.Directions.index(direction) + 2) % len(Op.Directions)]

    @staticmethod
    def turn_left(direction):
        return Op.Directions[(Op.Directions.index(direction) - 1) % len(Op.Directions)]

    @staticmethod
    def turn_right(direction):
        return Op.Directions[(Op.Directions.index(direction) + 1) % len(Op.Directions)]

    @staticmethod
    def move(departure, direction):
        x, y = departure
        dx, dy = direction
        return (x + dx, y + dy)


class Cart:
    def __init__(self, x, y, init_direction):
        self.x = x
        self.y = y
        self.d = init_direction
        self.choices = 0
        self.dead = False

    def move(self, grid):
        self.x, self.y = Op.move((self.x, self.y), self.d)
        connections = grid.site(self.x, self.y).connections
        if len(connections) == 4:
            choice = self.choices % 3
            if choice == 0:
                self.d = Op.turn_left(self.d)
            elif choice == 1:
                pass
            else:
                self.d = Op.turn_right(self.d)
            self.choices += 1
        else:
            self.d = next(iter(connections.difference({Op.opposite(self.d)})))


class Grid:
    def __init__(self, width, height, sites):
        self.sites = sites
        self.width = width
        self.height = height

    def site(self, x, y):
        return self.sites[(x, y)]

    def show(self, carts):
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                site = self.sites[(x, y)]
                if site is None or len(site.connections) == 0:
                    row.append(' ')
                elif len(site.connections) == 4:
                    row.append('+')
                else:
                    if site.connections == {Op.East, Op.West}:
                        row.append('-')
                    elif site.connections == {Op.North, Op.South}:
                        row.append('|')
                    elif (site.connections == {Op.East, Op.South}
                          or site.connections == {Op.North, Op.West}):
                        row.append('/')
                    elif (site.connections == {Op.North, Op.East}
                          or site.connections == {Op.West, Op.South}):
                        row.append('\\')
                    else:
                        row.append('!')
            rows.append(row)

        cart_symbol = {
            Op.East: '>',
            Op.South: 'v',
            Op.West: '<',
            Op.North: '^'
        }

        for cart in carts:
            if not cart.dead:
                rows[cart.y][cart.x] = cart_symbol[cart.d]

        print('\n'.join([''.join(row) for row in rows]))


def from_grid_text(text):
    chars = [list(line) for line in text.split('\n')]
    height = len(chars)
    width = max(len(row) for row in chars)

    cases = []
    for d in Op.Directions:
        cases.append(((d, '+'), (d, None)))
    for d in [Op.East, Op.West]:
        cases.append(((d, '-'), (d, None)))
    for d in [Op.North, Op.South]:
        cases.append(((d, '|'), (d, None)))
    cases += [
        ((Op.East, '\\'), (Op.South, None)),
        ((Op.South, '\\'), (Op.East, None)),
        ((Op.West, '\\'), (Op.North, None)),
        ((Op.North, '\\'), (Op.West, None))
    ]
    cases += [
        ((Op.East, '/'), (Op.North, None)),
        ((Op.North, '/'), (Op.East, None)),
        ((Op.West, '/'), (Op.South, None)),
        ((Op.South, '/'), (Op.West, None))
    ]

    cart_symbol = {
        '>': Op.East,
        'v': Op.South,
        '<': Op.West,
        '^': Op.North
    }

    for d, s in product(Op.Directions, cart_symbol.keys()):
        if (d, s) not in [(Op.East, '<'), (Op.South, '^'), (Op.West, '>'), (Op.North, 'v')]:
            cases.append(((d, s), (cart_symbol[s], cart_symbol[s])))
        else:
            cases.append(((d, s), (Op.opposite(cart_symbol[s]), cart_symbol[s])))

    guide = dict(cases)
    visited = defaultdict(set)
    carts = []

    def track_route(start):
        try:
            if chars[start[1]][start[0]] == '-':
                init_direction = Op.East
            elif chars[start[1]][start[0]] == '|':
                init_direction = Op.South
            else:
                return
        except IndexError:
            return

        pos = start
        direction = init_direction
        while True:
            if direction in visited[pos]:
                break
            visited[pos].add(direction)
            next_pos = Op.move(pos, direction)
            symbol = chars[next_pos[1]][next_pos[0]]
            if (direction, symbol) not in guide:
                print(f'pos {pos} direction {direction} next_pos {next_pos}')
            next_direction, cart_direction = guide[(direction, symbol)]
            visited[next_pos].add(Op.opposite(direction))
            pos = next_pos
            direction = next_direction
            if cart_direction:
                carts.append(Cart(next_pos[0], next_pos[1], cart_direction))

    for y in range(height):
        for x in range(width):
            track_route((x, y))

    sites = defaultdict(lambda: None)
    for pos, connections in visited.items():
        sites[pos] = Site(pos[0], pos[1], connections)

    return Grid(width, height, sites), carts
