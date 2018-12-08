from collections import defaultdict
from queue import PriorityQueue, Empty
from itertools import dropwhile


def parse_line(line):
    pieces = line.split(' ')
    return (pieces[1], pieces[7])


def inverse_graph(input):
    g = defaultdict(set)
    for parent, child in input:
        g[child].add(parent)
    return g


def solve_part1(input):
    tasks = sorted(list(set(t for p in input for t in p)))
    ig = inverse_graph(input)
    scheduled = ''
    while len(tasks) > 0:
        task = next(dropwhile(lambda t: not ig[t].issubset(set(scheduled)), tasks))
        scheduled += task
        tasks.remove(task)
    return scheduled


def task_time(task, task_time_base):
    return ord(task) - ord('A') + 1 + task_time_base


def solve_part2(input, n_workers, task_time_base):
    tasks = sorted(list(set(t for p in input for t in p)))
    workers = set(range(n_workers))
    ig = inverse_graph(input)
    done = ''
    events = PriorityQueue(len(tasks))
    time = 0

    print(ig)

    while True:
        try:
            event = events.get_nowait()
            time, task, worker = event
            done += task
            workers.add(worker)
        except Empty:
            pass

        available_tasks = list(filter(lambda t: ig[t].issubset(set(done)), tasks))

        print(f'time {time} available_tasks {available_tasks} ')

        scheduled_workers = set()
        scheduled_tasks = set()
        for worker, task in zip(workers, available_tasks):
            events.put((time + task_time(task, task_time_base), task, worker))
            print(f'assign task { task} to worker {worker} at time {time}')
            scheduled_workers.add(worker)
            scheduled_tasks.add(task)
        for task in scheduled_tasks:
            tasks.remove(task)
        for worker in scheduled_workers:
            workers.remove(worker)
        if events.empty():
            break
    return time, done
