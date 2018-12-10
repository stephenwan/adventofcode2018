from collections import namedtuple

Node = namedtuple('Node', 'children,meta')


def parse_line(line):
    return [int(e) for e in line.split(' ')]


def solve_part1(input):
    meta_sum = 0

    def callback(node):
        nonlocal meta_sum
        meta_sum += sum(node.meta)

    read_node(iter(input), callback=callback)
    return meta_sum


def solve_part2(input):
    root = read_node(iter(input))
    return node_value(root)


def node_value(node):
    if len(node.children) == 0:
        return sum(node.meta)

    return sum(node_value(node.children[m - 1])
               for m in node.meta
               if m > 0 and m <= len(node.children))


def read_node(gen, callback=None):
    n_children = next(gen)
    n_meta = next(gen)
    children = [read_node(gen, callback) for _ in range(n_children)]
    meta = [v for _, v in zip(range(n_meta), gen)]
    node = Node(children, meta)
    if callback is not None:
        callback(node)
    return node
