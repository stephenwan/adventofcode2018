from collections import deque


def bfs(start,
        lookup_children,
        key=None,
        on_node_add=None,
        on_node_begin=None,
        on_node_done=None,
        with_distance=False,
        with_path=False,
        depth_first=False):
    if key is None:
        key = lambda x: x

    output = []
    waiting_queue = deque()
    waiting_queue.append((start, 0))

    if with_path:
        seen = {key(start): [start]}
    else:
        seen = {key(start)}

    def enrich_node(node, distance, path):
        info = {'node': node}
        if with_distance:
            info['distance'] = distance
        if with_path:
            info['path'] = path
        return info

    while len(waiting_queue) > 0:
        if not depth_first:
            node, distance = waiting_queue.popleft()
        else:
            node, distance = waiting_queue.pop()
        rich_node = enrich_node(node, distance,
                                seen[key(node)] if with_path else None)

        output.append(rich_node)
        if on_node_begin is None or on_node_begin(**rich_node):
            children = lookup_children(node)
            if depth_first:
                children = reversed(children)
            for child in children:
                k = key(child)
                if k not in seen:
                    child_path = seen[key(node)] + [child] if with_path else None
                    if on_node_add is not None:
                        rich_child = enrich_node(child, distance + 1, child_path)
                        if not on_node_add(**rich_child):
                            continue
                    waiting_queue.append((child, distance + 1))
                    if with_path:
                        seen[k] = child_path
                    else:
                        seen.add(k)
            if on_node_done is not None:
                if not on_node_done(**rich_node):
                    break

    if not with_path and not with_distance:
        return [o['node'] for o in output]
    return output


def minmax(vs, with_idx=False):
    min_v, max_v = (None, None)
    idx_min, idx_max = (None, None)
    for i, v in enumerate(vs):
        if min_v is None or v < min_v:
            min_v = v
            idx_min = i
        if max_v is None or v > max_v:
            max_v = v
            idx_max = i

    if with_idx:
        return (min_v, idx_min), (max_v, idx_max)
    else:
        return min_v, max_v
