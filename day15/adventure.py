from collections import defaultdict


class Unit:
    def __init__(self, y, x):
        self.hp = 200
        self.damage = 3
        self.y = y
        self.x = x
        self.alive = True

    @property
    def p(self):
        return (self.y, self.x)

    def faction(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.faction()}{self.p}:{self.hp}'

    def __str__(self):
        return self.faction()[0]

    def move(self, grid):
        path = self.find_opponent_path(grid)
        if path is None or len(path) <= 2:
            return
        # print(f'{self.__repr__()} path {path}')
        grid.relocate(self, path[1])

    def attack(self, grid, check_death=None):
        opponents = self.in_range_opponents(grid)
        if len(opponents) == 0:
            return

        target = next(iter(sorted(opponents, key=lambda u: (u.hp, u.y, u.x))))
        print(f'{self} is attacking {target}')
        target.hp -= self.damage
        if target.hp <= 0:
            target.alive = False
            grid.remove(target)
            if check_death is not None:
                check_death(target)

    def find_opponent_path(self, grid):
        from lib.alg import bfs
        opponent, opponent_path = None, None

        def lookup_children(node):
            return Op.neighbours(node)

        def on_node_add(node, path):
            node = grid.cells[node]
            if isinstance(node, Empty):
                return True
            if isinstance(node, Unit) and node.faction() != self.faction():
                return True
            return False

        def on_node_done(node, path):
            node = grid.cells[node]
            nonlocal opponent, opponent_path
            if node != self and isinstance(node, Unit):
                opponent, opponent_path = (node, path)
                return False
            return True

        bfs(self.p, lookup_children=lookup_children,
            on_node_add=on_node_add, on_node_done=on_node_done,
            with_path=True)

        return opponent_path

    def in_range_opponents(self, grid):
        return [unit for p in Op.neighbours(self.p)
                for unit in [grid.cells[p]]
                if isinstance(unit, Unit) and unit.faction() != self.faction()]


class ElfDied(Exception):
    pass


class Elf(Unit):
    pass


class Goblin(Unit):
    pass


class Empty:
    def __str__(self):
        return '.'


class Wall:
    def __str__(self):
        return '#'


class Grid:
    def __init__(self, width, height, cells):
        self.width = width
        self.height = height
        self.cells = cells

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = ''.join([str(self.cells[(y, x)])
                            for x in range(self.width)])
            units_info = ' '.join([f'{self.cells[(y, x)]}: {self.cells[(y, x)].hp}'
                                   for x in range(self.width)
                                   if isinstance(self.cells[(y, x)], Unit)])
            lines.append(f'{line}\t\t{units_info}')
        return '\n'.join(lines)

    def relocate(self, unit, location):
        if not isinstance(unit, Unit):
            raise Exception(f'cannot move {unit}')
        if not isinstance(self.cells[location], Empty):
            raise Exception(f'cannot move to {location}')
        self.cells[unit.p], self.cells[location] = (self.cells[location],
                                                    self.cells[unit.p])
        unit.y, unit.x = location

    def remove(self, unit):
        if not isinstance(unit, Unit):
            raise Exception(f'cannot remove {unit}')
        self.cells[unit.p] = Empty()


class Op:
    East = (0, 1)
    South = (1, 0)
    West = (0, -1)
    North = (-1, 0)
    # Directions = [East, South, West, North]
    Directions = [North, West, East, South]

    @staticmethod
    def neighbour(current, direction):
        y, x = current
        dy, dx = direction
        return (y + dy, x + dx)

    @staticmethod
    def neighbours(current):
        return [Op.neighbour(current, d) for d in Op.Directions]


def from_map_text(text):
    cells = defaultdict(lambda: None)
    elves = []
    goblins = []
    lines = text.split('\n')
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == 'E':
                cells[(y, x)] = Elf(y, x)
                elves.append(cells[(y, x)])
            elif c == 'G':
                cells[(y, x)] = Goblin(y, x)
                goblins.append(cells[(y, x)])
            elif c == '.':
                cells[(y, x)] = Empty()
            else:
                cells[(y, x)] = Wall()
    grid = Grid(max(len(l) for l in lines), len(lines), cells)
    return grid, elves, goblins


def battle(grid, elves, goblins, check_death=None):
    tick = 0
    print(f'Round: {tick}')
    print(grid)
    units = elves + goblins
    battle_ended = False
    while not battle_ended:
        units = sorted(units, key=lambda unit: unit.p)
        for unit in units:
            if not unit.alive:
                continue
            if len(set(u.faction() for u in units if u.alive)) <= 1:
                battle_ended = True
                break
            unit.move(grid)
            unit.attack(grid, check_death)
        else:
            tick += 1
        units = [u for u in units if u.alive]
        print(f'\nRound: {tick}')
        print(grid)
    print(f'tick * {sum([u.hp for u in units if u.alive])}')
    return tick * sum([u.hp for u in units if u.alive])


def solve_part1(input_file):
    import lib.util as u
    text = u.get_input_from_file(input_file, break_lines=False)
    grid, elves, goblins = from_map_text(text)
    return battle(grid, elves, goblins)


def solve_part2(input_file):
    import lib.util as u
    text = u.get_input_from_file(input_file, break_lines=False)
    power = 3

    def check_death(unit):
        if isinstance(unit, Elf):
            raise ElfDied()

    while True:
        grid, elves, goblins = from_map_text(text)
        print(f'\n** Elf Power {power} **')
        for elf in elves:
            elf.damage = power
        try:
            return battle(grid, elves, goblins, check_death)
        except ElfDied:
            power += 1
