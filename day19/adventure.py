from collections import defaultdict


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


registers = [0] * 6


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
        while not self.halted:
            if shortcut is not None:
                shortcut(self)
            ori_first = self.rs[0]
            self.execute_once()
            aft_first = self.rs[0]
            if ori_first != aft_first:
                print(f'first changed: {self}')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ip={self.ipv} {self.rs}'


def solve_part1(file_path):
    ip, ins = from_file_data(file_path)
    d = Device(ip, ins)
    d.execute_forever()
    return d.rs[0]


def solve_part2(file_path):
    '''The key is to watch out the logical command that behaves like
 a *if* branch. The code inside the if block can be abbreviated using
shortcuts. The final logical commandmay be reduced with shortcut too,
but I haven't tried that because I already got the answer.

The final log was quite interesting:

first changed: ip=35 [0, 0, 10550400, 10551330, 34, 0]
first changed: ip=8 [1, 10551330, 1, 10551330, 7, 1]
first changed: ip=8 [3, 5275665, 1, 10551330, 7, 2]
first changed: ip=8 [6, 3517110, 1, 10551330, 7, 3]
first changed: ip=8 [11, 2110266, 1, 10551330, 7, 5]
first changed: ip=8 [17, 1758555, 1, 10551330, 7, 6]
first changed: ip=8 [26, 1172370, 1, 10551330, 7, 9]
first changed: ip=8 [36, 1055133, 1, 10551330, 7, 10]
first changed: ip=8 [51, 703422, 1, 10551330, 7, 15]
first changed: ip=8 [69, 586185, 1, 10551330, 7, 18]
first changed: ip=8 [96, 390790, 1, 10551330, 7, 27]
first changed: ip=8 [126, 351711, 1, 10551330, 7, 30]
first changed: ip=8 [171, 234474, 1, 10551330, 7, 45]
first changed: ip=8 [225, 195395, 1, 10551330, 7, 54]
first changed: ip=8 [315, 117237, 1, 10551330, 7, 90]
first changed: ip=8 [450, 78158, 1, 10551330, 7, 135]
first changed: ip=8 [720, 39079, 1, 10551330, 7, 270]
first changed: ip=8 [39799, 270, 1, 10551330, 7, 39079]
first changed: ip=8 [117957, 135, 1, 10551330, 7, 78158]
first changed: ip=8 [235194, 90, 1, 10551330, 7, 117237]
first changed: ip=8 [430589, 54, 1, 10551330, 7, 195395]
first changed: ip=8 [665063, 45, 1, 10551330, 7, 234474]
first changed: ip=8 [1016774, 30, 1, 10551330, 7, 351711]
first changed: ip=8 [1407564, 27, 1, 10551330, 7, 390790]
first changed: ip=8 [1993749, 18, 1, 10551330, 7, 586185]
first changed: ip=8 [2697171, 15, 1, 10551330, 7, 703422]
first changed: ip=8 [3752304, 10, 1, 10551330, 7, 1055133]
first changed: ip=8 [4924674, 9, 1, 10551330, 7, 1172370]
first changed: ip=8 [6683229, 6, 1, 10551330, 7, 1758555]
first changed: ip=8 [8793495, 5, 1, 10551330, 7, 2110266]
first changed: ip=8 [12310605, 3, 1, 10551330, 7, 3517110]
first changed: ip=8 [17586270, 2, 1, 10551330, 7, 5275665]
first changed: ip=8 [28137600, 1, 1, 10551330, 7, 10551330]


'''
    ip, ins = from_file_data(file_path)
    d = Device(ip, ins)
    d.rs[0] = 1

    def shortcut(device):
        if device.ipv == 3 and device.rs[4] == 2:
            if device.rs[1] * device.rs[5] <= device.rs[3]:
                device.rs[1] = int(device.rs[3] / device.rs[5])
        if device.ipv == 9 and device.rs[4] == 8:
            if device.rs[1] <= device.rs[3]:
                device.rs[1] = device.rs[3] + 1

    d.execute_forever(shortcut)
    return d.rs[0]
