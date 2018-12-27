import numpy as np
import pandas as pd


def from_file_data(file_path):
    from lib.util import get_input_from_file

    def parse_line(line):
        return (int(n) for n in line.split(','))

    tuples = get_input_from_file(file_path, parser=parse_line)
    return pd.DataFrame.from_records(tuples, columns=['x', 'y', 'z', 't'])


def mh_d(l, r):
    return np.abs(l['x_l'] - r['x_r']) \
        + np.abs(l['y_l'] - r['y_r']) \
        + np.abs(l['z_l'] - r['z_r']) \
        + np.abs(l['t_l'] - r['t_r'])


def in_range(df: pd.DataFrame):
    idx = pd.MultiIndex.from_product([df.index, df.index],
                                     names=['l', 'r'])
    pairs = pd.concat([df.add_suffix('_l').reindex(idx, level='l'),
                       df.add_suffix('_r').reindex(idx, level='r')],
                      axis=1)

    return (mh_d(pairs[['x_l', 'y_l', 'z_l', 't_l']],
                 pairs[['x_r', 'y_r', 'z_r', 't_r']]) <= 3)


def constellation(df: pd.DataFrame, in_range: pd.DataFrame):
    cons = pd.Series(np.full(len(df), -1), index=df.index)

    def get_cons_root(idx):
        cur = idx
        while cons[cur] != cur:
            cur = cons[cur]
        return cur

    for i, row in df.iterrows():
        idx_in_range = np.argwhere(in_range.loc[(i, slice(0, i - 1))]).flatten()
        cons[i] = i
        for idx in idx_in_range:
            root = get_cons_root(idx)
            cons[root] = cons[i]

    cons = pd.Series([get_cons_root(i) for i in cons.values],
                     index=cons.index)
    print(f'constellation {cons}')
    return len(set(cons.values))


def solve_part1(file_path):
    df = from_file_data(file_path)
    ir = in_range(df)
    return constellation(df, ir)


def solve_part2():
    # well...
    pass
