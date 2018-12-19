def solve_part1(input):
    return sum(input)


def solve_part2(input):
    size = len(input)
    subsums = {(0, 0): 0}
    for i in range(size):
        subsums[(0, i + 1)] = subsums[(0, i)] + input[i]

    for j in range(1, size + 1):
        for i in range(j):
            subsums[(i, j)] = subsums[(0, j)] - subsums[(0, i)]
            if subsums[(i, j)] == 0:
                return subsums[(0, i)]

    overflow_sums = {}
    for i in range(size):
        for j in range(size):
            overflow_sums[(i, j)] = subsums[(j, size)] + subsums[(0, i)]
            if overflow_sums[(i, j)] == 0:
                return subsums[(0, j)]

    total = subsums[(0, size)]
    least_rounds = None
    least_idx = None
    for (idx, v) in overflow_sums.items():
        if (v > 0) == (0 > total) and abs(v) % abs(total) == 0:
            rounds = abs(v) // abs(total)
            if least_rounds is None or rounds < least_rounds:
                least_rounds = rounds
                least_idx = idx

    if least_idx is None:
        print('No repeated value is found')
        return

    return subsums[(0, least_idx[1])]
