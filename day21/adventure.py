###############################################################################
#                       reduction to the operation flow                       #
###############################################################################


def step_10_to_12(rs4):
    return ((rs4 & 16777215) * 65899) & 16777215


def reduced_flow(rs4, initial_rs4, bootstrapping=False):
    if bootstrapping:
        rs3 = 0 | 65536
    else:
        rs3 = rs4 | 65536
    rs3_bytes = []
    rs3_bytes.append(rs3 & 255)
    rs3_bytes.append((rs3 >> 8) & 255)
    rs3_bytes.append((rs3 >> 16) & 255)
    result = initial_rs4
    for rs3_byte in rs3_bytes:
        result = step_10_to_12(rs3_byte + result)
    return result


def generate_rs4(initial_rs4):
    rs4 = initial_rs4
    bootstrapping = True
    while True:
        rs4 = reduced_flow(rs4, initial_rs4, bootstrapping)
        yield rs4
        bootstrapping = False


def solve_part1():
    initial_rs4 = 10552971
    return next(generate_rs4(initial_rs4))


def solve_part2():
    initial_rs4 = 10552971
    seen = set()
    last_added = None
    for value in generate_rs4(initial_rs4):
        if value not in seen:
            last_added = value
            seen.add(value)
        else:
            break
    return last_added


###############################################################################
#                 same as day19. used for validating halting.                 #
###############################################################################


def addr(rs, a, b, c):
    rs[c] = rs[a] + rs[b]


def addi(rs, a, b, c):
    rs[c] = rs[a] + b


def mulr(rs, a, b, c):
    rs[c] = rs[a] * rs[b]


def muli(rs, a, b, c):
    rs[c] = rs[a] * b


def banr(rs, a, b, c):
    rs[c] = rs[a] & rs[b]


def bani(rs, a, b, c):
    rs[c] = rs[a] & b


def borr(rs, a, b, c):
    rs[c] = rs[a] | rs[b]


def bori(rs, a, b, c):
    rs[c] = rs[a] | b


def setr(rs, a, b, c):
    rs[c] = rs[a]


def seti(rs, a, b, c):
    rs[c] = a


def gtir(rs, a, b, c):
    rs[c] = 1 if a > rs[b] else 0


def gtri(rs, a, b, c):
    rs[c] = 1 if rs[a] > b else 0


def gtrr(rs, a, b, c):
    rs[c] = 1 if rs[a] > rs[b] else 0


def eqir(rs, a, b, c):
    rs[c] = 1 if a == rs[b] else 0


def eqri(rs, a, b, c):
    rs[c] = 1 if rs[a] == b else 0


def eqrr(rs, a, b, c):
    rs[c] = 1 if rs[a] == rs[b] else 0


ops = [addr, addi, mulr, muli, banr, bani, borr, bori,
       setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def from_file_data(file_path):
    from lib.util import get_input_from_file
    ilines = iter(get_input_from_file(file_path))
    ip = int(next(ilines).split(' ')[1])
    instructions = []
    for line in ilines:
        op_name, *params = line.split(' ')
        op = [op for op in ops if op.__name__ == op_name][0]
        instructions.append((op, list(map(int, params))))

    return ip, instructions


class Device:
    def __init__(self, ip, instructions):
        self.ip = ip
        self.instructions = instructions
        self.rs = [0] * 6
        self.ipv = 0
        self.halted = False

    def execute_once(self):
        try:
            op, params = self.instructions[self.ipv]
        except IndexError:
            self.halted = True
            return

        self.rs[self.ip] = self.ipv
        op(self.rs, *params)
        self.ipv = self.rs[self.ip] + 1

    def execute_forever(self, shortcut=None):
        i = 0
        while not self.halted:
            i += 1
            if shortcut is not None:
                shortcut(self)
            self.execute_once()
        return i

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ip={self.ipv} {self.rs}'

    def print_manual(self):
        for i, ins in enumerate(self.instructions):
            command, params = ins
            print(f'[{i}] {command.__name__} {params}')


def validate_termination(file_path, initial_0):
    import math

    def shortcuts(device):
        if device.ipv == 20:
            # print(f'20 - {device}')
            # [18] addi [5, 1, 2]
            # [19] muli [2, 256, 2]
            # [20] gtrr [2, 3, 2]
            if device.rs[2] <= device.rs[3]:
                device.rs[5] = math.floor(device.rs[3] / 256)
                device.rs[2] = (device.rs[5] + 1) * 256
        if device.ipv == 28:
            print(f'28:  {device}')

    ip, ins = from_file_data(file_path)
    d = Device(ip, ins)
    d.rs[0] = initial_0
    d.execute_forever(shortcuts)
    return d
