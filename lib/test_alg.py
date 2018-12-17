from lib.alg import bfs


def test_bfs():
    graph = {
        3: [1, 4],
        1: [5, 7],
        4: [9],
        9: [10],
        10: [12, 16]
    }

    def lookup_children(node):
        if node not in graph:
            return []
        return graph[node]

    result = bfs(3, lookup_children, with_path=True, with_distance=True)
    transformed = [(o['node'], o['distance'], o['path']) for o in result]
    assert transformed == [(3, 0, [3]), (1, 1, [3, 1]), (4, 1, [3, 4]),
                           (5, 2, [3, 1, 5]), (7, 2, [3, 1, 7]), (9, 2, [3, 4, 9]),
                           (10, 3, [3, 4, 9, 10]), (12, 4, [3, 4, 9, 10, 12]),
                           (16, 4, [3, 4, 9, 10, 16])]


def test_bfs_on_node_begin():
    graph = {
        3: [1, 4],
        1: [5, 7],
        4: [9],
        9: [10],
        10: [12, 16]
    }

    def lookup_children(node):
        if node not in graph:
            return []
        return graph[node]

    def on_node_begin(node):
        if node % 2 == 0:
            return False
        return True

    result = bfs(3, lookup_children, on_node_begin=on_node_begin)
    assert result == [3, 1, 4, 5, 7]


def test_bfs_on_node_add():
    graph = {
        3: [1, 4],
        1: [5, 7],
        4: [9],
        9: [10],
        10: [12, 16]
    }

    def lookup_children(node):
        if node not in graph:
            return []
        return graph[node]

    def on_node_add(node, distance):
        if distance > 1:
            return False
        return True

    result = bfs(3, lookup_children, on_node_add=on_node_add, with_distance=True)
    transformed = [o['node'] for o in result]
    assert transformed == [3, 1, 4]


def test_bfs_on_node_done():
    graph = {
        3: [1, 4],
        1: [5, 7],
        4: [9],
        9: [10],
        10: [12, 16]
    }

    def lookup_children(node):
        if node not in graph:
            return []
        return graph[node]

    def on_node_done(node):
        if node == 7:
            return False
        return True

    result = bfs(3, lookup_children, on_node_done=on_node_done)
    assert result == [3, 1, 4, 5, 7]


def test_dfs():
    graph = {
        3: [1, 4],
        1: [5, 7],
        4: [9],
        9: [10],
        10: [12, 16]
    }

    def lookup_children(node):
        if node not in graph:
            return []
        return graph[node]

    result = bfs(3, lookup_children, depth_first=True)
    assert result == [3, 1, 5, 7, 4, 9, 10, 12, 16]
