import string


reagents = set(zip((string.ascii_lowercase + string.ascii_uppercase),
                   (string.ascii_uppercase + string.ascii_lowercase)))


def solve_part1(input):
    length = 0
    remaining = input
    while length != len(remaining):
        length = len(remaining)
        remaining = remove_reacted(remaining)
    return len(remaining)


def solve_part2(input):
    lengths = []
    for defect1, defect2 in zip(string.ascii_lowercase, string.ascii_uppercase):
        wo_defects = ''.join((unit for unit in input
                              if unit != defect1 and unit != defect2))
        lengths.append(solve_part1(wo_defects))
    return min(lengths)


def remove_reacted(input):
    pos, cur, fwd = (0, 0, 1)
    reactives = []
    remaining = ''
    while cur < len(input) - 1:
        if (input[cur], input[fwd]) not in reagents:
            cur += 1
            fwd += 1
            continue
        fwd += 1
        bac = cur - 1
        while (bac >= pos and fwd < len(input) and
               (input[bac], input[fwd]) in reagents):
            fwd += 1
            bac -= 1
        reactives.append((bac + 1, fwd - 1))
        remaining = remaining + input[pos:(bac + 1)]
        pos, cur = (fwd, fwd)
        fwd = cur + 1
    remaining = remaining + input[pos:]
    return remaining
