from collections import Counter


def solve_part1(input):
    occ_counter = Counter()
    for line in input:
        line_counter = _part1_process_line(line)
        occ_counter.update(line_counter)
    prod = 1
    for v in occ_counter.values():
        prod = prod * v
    return prod


def _part1_process_line(line):
    return set(Counter(line).values()) - {1}


def solve_part2(input):
    known_shortened = set()
    for line in input:
        shortened = _part2_process_line(line)
        intersection = known_shortened.intersection(shortened)
        if len(intersection) > 0:
            return next(iter(intersection))
        known_shortened = known_shortened.union(shortened)
    print('No correct ID found.')


def _part2_process_line(line):
    shortened = set()
    for i in range(len(line)):
        shortened.add(line[:i] + line[i+1:])
    return shortened
