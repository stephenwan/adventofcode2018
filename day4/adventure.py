from collections import namedtuple, defaultdict
from datetime import datetime
import operator


Info = namedtuple('Data', 'id,awake')
Record = namedtuple('Record', 'datetime,info')


def parse_line(line):
    dt = datetime.fromisoformat(line[1:17])
    words = line[19:].split(' ')
    id = None
    if words[0] == 'wakes':
        awake = True
    elif words[0] == 'falls':
        awake = False
    else:
        awake = True
        id = int(words[1].lstrip('#'))

    return Record(datetime=dt, info=Info(id, awake))


def solve_part1(input):
    stats = build_stats(input)
    stats_total = dict((k, sum(v.values())) for k, v in stats.items())
    id = find_keymax(stats_total)
    time = find_keymax(stats[id])
    print(f'id {id} time {time}')
    return id * time


def solve_part2(input):
    stats = build_stats(input)
    stats_max = dict((k, max(v.values())) for k, v in stats.items())
    id = find_keymax(stats_max)
    time = find_keymax(stats[id])
    print(f'id {id} time {time}')
    return id * time


def find_keymax(d):
    return max(d.items(), key=operator.itemgetter(1))[0]


def build_stats(input):
    records = sorted(input, key=lambda r: r.datetime)
    cur_id = None
    timing_start = None
    stats = defaultdict(dict)
    for record in records:
        if record.info.id is not None:
            cur_id = record.info.id
        elif not record.info.awake:
            timing_start = record.datetime.minute
        else:
            timing_end = record.datetime.minute
            for t in range(timing_start, timing_end):
                stats[cur_id][t] = stats[cur_id].get(t, 0) + 1
    return stats
