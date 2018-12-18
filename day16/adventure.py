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


def parse_ops_input(path):
    import lib.util as u
    text = u.get_input_from_file(path, break_lines=False)
    segments = text.split('\n\n')
    result = []
    for seg in segments:
        lines = seg.split('\n')
        if len(lines) < 3:
            continue
        rs_start = [int(lines[0][i]) for i in (9, 12, 15, 18)]
        op_code, *op_input = lines[1].split(' ')
        op_code = int(op_code)
        op_input = [int(i) for i in op_input]
        rs_end = [int(lines[2][i]) for i in (9, 12, 15, 18)]
        result.append((op_code, op_input, rs_start, rs_end))
    return result


def parse_program_input(path):
    import lib.util as u
    lines = u.get_input_from_file(path)
    result = []
    for line in lines:
        op_code, *op_input = line.split(' ')
        result.append((int(op_code), [int(i) for i in op_input]))
    return result


def run_samples(cases):
    outcome = defaultdict(bool)
    for case in cases:
        op_code, op_input, rs_start, rs_end = case
        for i, op in enumerate(ops):
            rs = rs_start.copy()
            op(rs, *op_input)
            outcome[(i, op_code)] = rs == rs_end

    evidence = defaultdict(set)
    for (i, op_code), ok in outcome.items():
        if ok:
            evidence[i].add(op_code)
    return evidence


def solve_op_codes(evidence):
    op_idxes = sorted(evidence.keys(), key=lambda k: len(evidence[k]))

    def match_code(seen, matches):
        nonlocal evidence
        progress = dict(matches)
        for i in op_idxes:
            if i in matches:
                continue
            remaining = evidence[i].difference(seen)
            if len(remaining) == 0:
                return False, None
            for pick in remaining:
                if pick in progress.values():
                    next_matches = dict(matches)
                    next_matches[i] = pick
                    matched, return_matches = match_code({*seen, pick}, next_matches)
                    if matched:
                        return matched, return_matches
                else:
                    progress[i] = pick
                    break
            if i not in progress:
                return False, None
        return True, progress

    return match_code(set(), dict())


def solve_part1(ops_path):
    cases = parse_ops_input(ops_path)
    counts = []
    for case in cases:
        count = 0
        op_code, op_input, rs_start, rs_end = case
        for i, op in enumerate(ops):
            rs = rs_start.copy()
            op(rs, *op_input)
            if rs == rs_end:
                count += 1
        counts.append(count)
    return counts
    return len([c for c in counts if c >= 3])


def solve_part2(ops_path, program_path):
    cases = parse_ops_input(ops_path)
    evidence = run_samples(cases)
    solved, mapping = solve_op_codes(evidence)

    if not solved:
        return None

    print(str(mapping))

    matched = dict((v, k) for k, v in mapping.items())
    program = parse_program_input(program_path)
    rs = [0, 0, 0, 0]
    for ops_code, ops_input in program:
        ops[matched[ops_code]](rs, *ops_input)

    return rs
