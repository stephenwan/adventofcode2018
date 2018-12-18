from collections import Counter
import numpy as np
from numpy.lib.stride_tricks import as_strided


Ground = '.'
Tree = '|'
Lumberyard = '#'

center = (1, 1)
check_pos = np.ones((3, 3), dtype=bool)
check_pos[center] = False


def evolve(ground):
    windows = to_windows(ground)
    result = np.zeros(ground.shape, dtype='<U1')
    for i, j in np.ndindex(*ground.shape):
        result[i, j] = window_output(windows[i, j])
    return result


def to_windows(ground):
    padded = np.pad(ground, ((1,), (1,)), 'constant',
                    constant_values=('.',))
    return as_strided(padded, padded.shape + (3, 3), padded.strides * 2)


def window_output(window):
    counter = Counter(window[check_pos])
    current = window[center]

    if current == Ground:
        return Tree if counter[Tree] >= 3 else Ground
    elif current == Tree:
        return Lumberyard if counter[Lumberyard] >= 3 else Tree
    else:
        return (Lumberyard if counter[Tree] >= 1 and counter[Lumberyard] >= 1
                else Ground)


def to_str(ground):
    return '\n'.join(np.apply_along_axis(lambda a: ''.join(a),
                                         axis=1,
                                         arr=ground))


def solve_part1(ground, t):
    for _ in range(t):
        ground = evolve(ground)
    print(to_str(ground))
    c = Counter(ground.flat)
    return ground, c[Tree] * c[Lumberyard]


def solve_part2():
    '''Target time is 1000000000. Found the pattern repeats every 700 minutes
from minute 1000, which extrapolates to the target time.'''
    pass


def from_file_data(file_path):
    import lib.util as u
    lines = u.get_input_from_file(file_path)
    size = len(lines)
    return np.array(list(''.join(lines))).reshape(size, size)
