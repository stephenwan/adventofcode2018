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
        _, path = self.find_opponent_path(grid)
        if path is None or len(path) <= 2:
            return False
        # print(f'{self.__repr__()} path {path}')
        grid.relocate(self, path[1])
        return True

    def attack(self, grid, check_death=None):
        _, oppo, _ = self.partition(Op.neighbours(self.p), grid)
        if len(oppo) == 0:
            return False
        opponents = [grid.cells[u] for u in oppo]
        target = next(iter(sorted(opponents, key=lambda u: (u.hp, u.y, u.x))))
        print(f'{self} is attacking {target}')
        target.hp -= self.damage
        if target.hp <= 0:
            target.alive = False
            grid.remove(target)
            if check_death is not None:
                check_death(target)
        return True

    def find_opponent_path(self, grid):
        front = {self.p: [self.p]}
        seen = set(self.p)
        distance = 0
        while True:
            distance += 1
            oppo_paths = []
            new_front = {}
            new_seen = set()
            for p, trajectory in front.items():
                same, oppo, empty = self.partition([n for n in Op.neighbours(p)
                                                    if n not in seen], grid)
                if len(oppo) > 0:
                    for n in oppo:
                        oppo_paths.append(trajectory + [n])
                        # TODO: this part has bug. Need same handling as 'empty'
                elif len(empty) > 0:
                    for n in empty:
                        new_trajectory = trajectory + [n]
                        if n not in new_front:
                            new_front[n] = new_trajectory
                        else:
                            new_front[n] = min(new_trajectory, new_front[n])
                        new_seen.add(n)
            seen.update(new_seen)
            if len(oppo_paths) > 0:
                return distance, sorted(oppo_paths)[0]
            if len(new_front) == 0:
                return distance, None
            front = new_front

    def partition(self, positions, grid):
        partitions = defaultdict(list)
        for p in positions:
            cell = grid.cells[p]
            if isinstance(cell, Wall):
                pass
            elif isinstance(cell, Empty):
                partitions['empty'].append(p)
            elif cell.faction() == self.faction():
                partitions['same'].append(p)
            else:
                partitions['opposite'].append(p)
        return partitions['same'], partitions['opposite'], partitions['empty']


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
    Directions = [East, South, West, North]

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
    while True:
        tick += 1
        print(f'\nRound: {tick}')
        units = sorted(units, key=lambda unit: unit.p)
        moved = False
        attacked = False
        for unit in units:
            if not unit.alive:
                continue
            moved = unit.move(grid) or moved
            attacked = unit.attack(grid, check_death) or attacked
        print(f'moved {moved} attacked {attacked}')
        units = [u for u in units if u.alive]
        print(grid)
        if len(set(u.faction() for u in units)) <= 1:
            break
    print(f'{tick - 1} * {sum([u.hp for u in units if u.alive])}')
    return (tick - 1) * sum([u.hp for u in units if u.alive])


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
