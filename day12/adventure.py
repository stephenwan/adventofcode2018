import numpy as np

strd = np.lib.stride_tricks.as_strided


def parse_line(line):
    pieces = line.split(' => ')
    pattern = [c == '#' for c in pieces[0].strip()]
    outcome = pieces[1].strip() == '#'
    return (pattern, outcome)


def parse_initial(line):
    return [c == '#' for c in line.strip()]


def build_fertile_patterns(pattern_input):
    return np.array(list(pattern for pattern, result in pattern_input if result))


class Evolution():
    def __init__(self, pattern_strings, initial_string):
        patterns = [parse_line(s) for s in pattern_strings]
        self.patterns = build_fertile_patterns(patterns)
        self.state = (0, parse_initial(initial_string))

    def match_fertile(self, p):
        return not np.all(np.any(np.logical_xor(self.patterns, p), axis=1))

    def evolve(self):
        zero_offset, pods = Evolution.pad_state(self.state)
        pods_ = strd(pods, shape=(len(pods) - 4, 5), strides=(1, 1))
        pods_next = np.apply_along_axis(self.match_fertile, arr=pods_, axis=1)
        self.state = (zero_offset - 2, pods_next)
        return self.state

    def score(self):
        zero_offset, pods = self.state
        pod_values = np.arange(-zero_offset, len(pods) - zero_offset)
        return np.sum(pod_values[pods])

    @staticmethod
    def pad_state(state):
        zero_offset, pods = state
        left = Evolution.pad_length(pods, False)
        right = Evolution.pad_length(pods, True)
        if left == 0 and right == 0:
            return state
        padded_pods = np.pad(pods, (left, right),
                             mode='constant',
                             constant_values=(False,))
        return zero_offset + left, padded_pods

    @staticmethod
    def pad_length(pods, is_right):
        try:
            if is_right:
                return np.argwhere(pods[-4:]).flatten()[-1] + 1
            else:
                return 4 - np.argwhere(pods[:4]).flatten()[0]
        except IndexError:
            return 0

    def state_str(self):
        zero_offset, pods = self.state
        return ''.join([
            f'{">" if i == zero_offset else ""}{"#" if v else "."} '
            for i, v in enumerate(pods)]
        )


def solve_part1(pattern_str, initial_str):
    e = Evolution(pattern_str.split('\n'), initial_str)
    for _ in range(20):
        e.evolve()
    return e.score()


def solve_part2(pattern_str, initial_str):
    e = Evolution(pattern_str.split('\n'), initial_str)
    for i in range(50000000000):
        e.evolve()
        if i % 10000 == 1:
            print(f'round {i} done:\t{e.state_str()}')
            print(f'score: {e.score()} zero_offset: {e.state[0]}')

    return Evolution.score(e.state)
