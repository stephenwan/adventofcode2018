from collections import defaultdict


class Square:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    @property
    def p(self):
        return (self.y, self.x)

    @property
    def down(self):
        return (self.y + 1, self.x)

    @property
    def left(self):
        return (self.y, self.x - 1)

    @property
    def right(self):
        return (self.y, self.x + 1)

    @property
    def up(self):
        return (self.y - 1, self.x)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.y}, {self.x})'

    def __str__(self):
        return None


class Spring(Square):
    def __str__(self):
        return '+'


class Sand(Square):
    def __str__(self):
        return '.'


class Clay(Square):
    def __str__(self):
        return '#'


class Water(Square):
    def __init__(self, y, x, rest):
        super().__init__(y, x)
        self.rest = rest

    def __str__(self):
        return '~' if self.rest else '|'

    def __hash__(self):
        return hash(self.p)

    def __eq__(self, other):
        return self.p == other.p

    def drip(self, ground):
        if self not in ground.driplets:
            raise Exception(f'not a driplet {repr(self)}')

        done = any(f(self) for f in [ground.water_drop,
                                     ground.water_splash,
                                     ground.water_sink])

        if done:
            print(f'driplet {repr(self)} dripped')
        else:
            raise Exception(f'driplet not dripped {repr(self)}')


class Ground:
    def __init__(self, vrange, hrange, clay_pos, spring_pos=(0, 500)):
        self.vrange = vrange
        self.v_lo, self.v_hi = (min(vrange), max(vrange))
        self.hrange = hrange
        self.h_lo, self.h_hi = (min(hrange), max(hrange))
        self.squares = defaultdict(lambda: None)
        for y in vrange:
            for x in hrange:
                self.squares[y, x] = Sand(y, x)
        for p in clay_pos:
            self.squares[p] = Clay(*p)
        spring = Spring(*spring_pos)
        initial_driplet = Water(*spring.down, False)
        self.squares[spring.p] = spring
        self.squares[initial_driplet.p] = initial_driplet
        self.driplets = {initial_driplet}

    def __str__(self):
        lines = []
        for y in self.vrange:
            line = ''.join([str(self.squares[y, x]) for x in self.hrange])
            lines.append(line)
        return '\n'.join(lines)

    def at_bottom(self, driplet):
        return driplet.y == self.v_hi

    def water_drop(self, driplet):
        if self.at_bottom(driplet):
            self.driplets.remove(driplet)
            return True
        square = driplet
        driplet_merged = False
        while True:
            if self.at_bottom(square):
                break

            if self._check_moving_water(square.down):
                driplet_merged = True

            if isinstance(self.squares[square.down], Sand):
                self.squares[square.down] = Water(*square.down, False)
                square = self.squares[square.down]
            else:
                break

        if driplet != square or driplet_merged:
            self.driplets.remove(driplet)
            if not driplet_merged:
                self.driplets.add(square)
            return True
        else:
            return False

    def _check_moving_water(self, p):
        if not isinstance(self.squares[p], Water):
            return False
        return not self.squares[p].rest

    def _find_brims_and_walls(self, p):
        py, px = p
        left_range, right_range = (range(px - 1, self.h_lo - 1, -1),
                                   range(px + 1, self.h_hi + 1))

        def inspect(rg):
            for x in rg:
                target = self.squares[(py, x)]
                if isinstance(target, Clay):
                    return ('wall', x)
                if self._check_moving_water(target.down):
                    return ('brim', x)
                if isinstance(self.squares[target.down], Sand):
                    return ('brim', x)
            raise Exception(f'no brim or wall {repr(p)} {py},{min(rg)}-{max(rg)}')

        return (inspect(left_range), inspect(right_range))

    def water_splash(self, driplet):
        left, right = self._find_brims_and_walls(driplet.p)
        if left[0] == 'wall' and right[0] == 'wall':
            return False
        left_start = left[1] + 1 if left[0] == 'wall' else left[1]
        right_end = right[1] - 1 if right[0] == 'wall' else right[1]
        for x in range(left_start, right_end + 1):
            self.squares[driplet.y, x] = Water(driplet.y, x, False)
        self.driplets.remove(driplet)
        if left[0] == 'brim':
            self.driplets.add(self.squares[driplet.y, left[1]])
        if right[0] == 'brim':
            self.driplets.add(self.squares[driplet.y, right[1]])
        return True

    def water_sink(self, driplet):
        square = driplet
        while True:
            left, right = self._find_brims_and_walls((square.y, driplet.x))
            if left[0] != 'wall' or right[0] != 'wall':
                break
            rg = range(left[1] + 1, right[1])
            if any(isinstance(self.squares[square.y, x], Clay)
                   for x in rg):
                break
            for x in rg:
                self.squares[square.y, x] = Water(square.y, x, True)
            self.driplets.remove(square)
            self.driplets.add(self.squares[square.up])
            square = self.squares[square.up]

        if driplet == square:
            return False
        else:
            if isinstance(square, Sand):
                self.driplets.remove(square)
                self.squares[square.p] = Water(*square.p, False)
                self.driplets.add(self.squares[square.p])
            return True


def solve_part_1_and_2(text, output_file=None):
    ground, (ylo, yhi) = from_text_data(text)

    while len(ground.driplets) > 0:
        driplet = next(iter(ground.driplets))
        driplet.drip(ground)

    if output_file is not None:
        dump_ground_to_file(ground, output_file)
    part_1_result = 0
    part_2_result = 0
    for y in range(ylo, yhi + 1):
        for x in ground.hrange:
            if isinstance(ground.squares[y, x], Water):
                part_1_result += 1
                if ground.squares[y, x].rest:
                    part_2_result += 1

    return part_1_result, part_2_result


def dump_ground_to_file(ground, file_path):
    with open(file_path, 'w') as f:
        f.write(str(ground))


def parse_line(line):
    import re
    pattern = r'([xy])=(\d+),\s([xy])=(\d+)[.]{2}(\d+)'
    matches = re.match(pattern, line.strip())
    s1, v, s2, lo, hi = matches.groups()
    if s1 == 'x':
        return [(y, int(v)) for y in range(int(lo), int(hi) + 1)]
    else:
        return [(int(v), int(x)) for x in range(int(lo), int(hi) + 1)]


def from_file_data(file_path):
    from lib.util import get_input_from_file
    text = get_input_from_file(file_path, break_lines=False)
    return from_text_data(text)


def from_text_data(text):
    line_records = [parse_line(line) for line in text.split('\n')]
    clay_pos = [record for records in line_records for record in records]
    ylo = min(y for y, _ in clay_pos)
    yhi = max(y for y, _ in clay_pos)
    vrange = range(0, yhi + 1)
    xlo = min(x for _, x in clay_pos) - 2
    xhi = max(x for _, x in clay_pos) + 2
    hrange = range(xlo, xhi + 1)
    return Ground(vrange, hrange, clay_pos), (ylo, yhi)
