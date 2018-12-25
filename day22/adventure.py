from functools import lru_cache
from lib.util import timeit
from lib.geo import Point
from queue import PriorityQueue, Empty


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target

    @lru_cache(maxsize=None)
    def geo_idx(self, p):
        if p == Point(0, 0) or p == self.target:
            return 0
        if p.y == 0:
            return p.x * 16807
        if p.x == 0:
            return p.y * 48271
        return self.erosion_lvl(p.north) * self.erosion_lvl(p.west)

    def erosion_lvl(self, p):
        return (self.geo_idx(p) + self.depth) % 20183

    @lru_cache(maxsize=None)
    def risk_lvl(self, p):
        return self.erosion_lvl(p) % 3

    @timeit
    def total_risk_lvl(self):
        ty, tx = (self.target.y, self.target.x)
        return sum(self.risk_lvl(Point(y, x))
                   for y in range(ty + 1)
                   for x in range(tx + 1))


def solve_part1():
    cave = Cave(8112, Point(743, 13))
    return cave.total_risk_lvl()


class Rescue:
    def __init__(self, cave):
        self.cave = cave
        self.change_cost = 7
        self.cost_cache = {}

    @lru_cache(maxsize=None)
    def equips(self, p):
        # 0 : neither not compatible with 0 rocky
        # 1 : torch not compatible with 1 wet
        # 2 : ladder not compatible with 2 narrow
        return set(i for i in range(3) if i != self.cave.risk_lvl(p))

    def compare_equips(self, p, n):
        p_equips = self.equips(p)
        n_equips = self.equips(n)
        common = p_equips.intersection(n_equips)
        if len(common) == 2:
            return True, common
        else:
            p_uniq = p_equips - n_equips
            q_uniq = n_equips - p_equips
            return False, (next(iter(common)),
                           next(iter(p_uniq)),
                           next(iter(q_uniq)))

    def alt(self, p, equip):
        return (self.equips(p) - {equip}).pop()

    def update_cost_cache(self, p, cost, equip):
        alt_equip = self.alt(p, equip)
        alt_cost = cost + self.change_cost
        updated_equips = set()
        if p not in self.cost_cache:
            self.cost_cache[p] = {}
            self.cost_cache[p][equip] = cost
            self.cost_cache[p][alt_equip] = alt_cost
            updated_equips.update({equip, alt_equip})
        else:
            if cost < self.cost_cache[p][equip]:
                self.cost_cache[p][equip] = cost
                updated_equips.add(equip)
            if alt_cost < self.cost_cache[p][alt_equip]:
                self.cost_cache[p][alt_equip] = alt_cost
                updated_equips.add(alt_equip)
        return updated_equips

    def fastest_first_search(self, start, start_equip, limit=None):
        self.update_cost_cache(start, 0, start_equip)
        queue = PriorityQueue()
        for equip, cost in self.cost_cache[start].items():
            queue.put((cost, start, equip))

        def estimate_neighbour_cost(p, n, equip):
            p_cost = self.cost_cache[p][equip]
            if equip in self.equips(n):
                return p_cost + 1, equip
            else:
                return p_cost + 1 + self.change_cost, self.alt(p, equip)

        while True:
            try:
                cost, p, equip = queue.get_nowait()
            except Empty:
                break

            if p == self.cave.target:
                if equip == start_equip:
                    limit = cost
                else:
                    limit = cost + self.change_cost

            for n in p.neighbours():
                if n.x < 0 or n.y < 0:
                    continue
                cost, n_equip = estimate_neighbour_cost(p, n, equip)
                if limit is not None and cost > limit:
                    continue

                updated_equips = self.update_cost_cache(n, cost, n_equip)
                for e in updated_equips:
                    queue.put((cost, n, e))

        return self.cost_cache[self.cave.target][start_equip]


def solve_part2():
    cave = Cave(8112, Point(743, 13))
    rescue = Rescue(cave)
    return rescue.fastest_first_search(Point(0, 0), 1)
