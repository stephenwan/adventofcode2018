import numpy as np


def grid(serial, size):
    grid = np.zeros((size, size))
    x = np.arange(0, size) + 1
    y = np.arange(0, size).reshape((size, 1)) + 1
    rack = x + 10
    return np.floor(((grid + rack) * y + serial) * rack % 1000 / 100 - 5)


def conv2d(a, f):
    s = f.shape + tuple(np.subtract(a.shape, f.shape) + 1)
    strd = np.lib.stride_tricks.as_strided
    subM = strd(a, shape=s, strides=a.strides * 2)
    return np.einsum('ij,ijkl->kl', f, subM).astype(int)


def solve_part1(serial, size):
    g = grid(serial, size)
    conved = conv2d(g, np.ones((3, 3)))
    i, j = np.unravel_index(np.argmax(conved, axis=None), conved.shape)
    return (j + 1, i + 1), conved[i][j]


def solve_part2(serial, size):
    g = grid(serial, size)
    max_v, max_idx = (None, None)
    for s in range(size):
        conved = conv2d(g, np.ones((s + 1, s + 1)))
        i, j = np.unravel_index(np.argmax(conved, axis=None), conved.shape)
        print(f'{j + 1},{i + 1},{s} : {conved[i][j]}')
        if conved[(i, j)] < -200:
            break
        if max_v is None or conved[(i, j)] > max_v:
            max_v = conved[(i, j)]
            max_idx = (j + 1, i + 1, s)
    return max_idx, max_v
