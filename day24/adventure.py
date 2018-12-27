import math


class UnitGroup:
    def __init__(self, identity, faction, units, hp, ap, dmg_type,
                 initiative, weakness=None, immune=None, boost=0):
        self.id = identity
        self.faction = faction
        self.units = units
        self.hp = hp
        self.ap = ap
        self.dmg_type = dmg_type
        self.initiative = initiative
        self.weakness = weakness or set()
        self.immune = immune or set()
        self.boost = boost
        self.target = None

    def set_target(self, unit_group):
        self.target = unit_group

    def clear_target(self):
        self.target = None

    @property
    def power(self):
        return self.units * (self.ap + self.boost)

    @property
    def alive(self):
        return self.units > 0

    def receive_damage(self, damage):
        unit_loss = min(math.floor(damage / self.hp), self.units)
        self.units = self.units - unit_loss
        return unit_loss

    def damage(self, defending):
        if self.faction == defending.faction:
            return 0
        if self.dmg_type in defending.weakness:
            return self.power * 2
        elif self.dmg_type in defending.immune:
            return 0
        else:
            return self.power

    def damage_target(self):
        if self.target is None:
            return 0
        return self.target.receive_damage(self.damage(self.target))

    def __repr__(self):
        return f'{self.faction} [{self.id}] {self.units} units ' \
            + f'hp {self.hp} ap {self.ap}-{self.dmg_type} ' \
            + f'<{self.weakness} >{self.immune} ' \
            + f'i({self.initiative})'

    def __str__(self):
        return self.__repr__()


class Battle:
    def __init__(self, unit_groups, boost_immune=0):
        self.unit_groups = sorted(unit_groups, key=lambda x: x.initiative,
                                  reverse=True)
        if boost_immune > 0:
            for g in self.faction('Immune'):
                g.boost = boost_immune

    def faction(self, faction):
        return [ug for ug in self.unit_groups if ug.faction == faction]

    def match_targets(self):
        targeted = set()
        ordered = sorted(self.unit_groups,
                         key=lambda g: (g.power, g.initiative),
                         reverse=True)

        for group in ordered:
            if not group.alive:
                continue

            untargeted = [g for g in self.unit_groups if g
                           not in targeted and g.alive and g.faction != group.faction]
            score, target = max([((group.damage(g), g.power), g) for g in untargeted],
                                key=lambda t: t[0],
                                default=(None, None))
            if target is None or score[0] == 0:
                continue
            group.set_target(target)
            targeted.add(target)

    def clear_targets(self):
        for g in self.unit_groups:
            g.clear_target()

    def targets_attack(self):
        total_loss = 0
        for g in self.unit_groups:
            if not g.alive:
                continue
            total_loss += g.damage_target()
        return total_loss

    def remains(self, faction):
        return any(g for g in self.unit_groups
                   if g.faction == faction and g.alive)

    def run(self):
        i = 0
        while self.remains('Immune') and self.remains('Infection'):
            # print(f'\n****** round {i}******\n')
            # print(f'\n{repr(self)}\n')
            self.match_targets()
            total_loss = self.targets_attack()
            if total_loss == 0:
                break
            self.clear_targets()
            i += 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        pieces = []
        for faction in ['Immune', 'Infection']:
            for ug in sorted(self.faction(faction), key=lambda x: x.id):
                pieces.append(f'{repr(ug)}')
        return '\n'.join(pieces)


def from_file_data(file_path):
    from lib.util import get_input_from_file

    text = get_input_from_file(file_path, break_lines=False)
    factions = text.split('\n\n')

    result = []
    for faction in factions:
        lines = faction.split('\n')
        if lines[0].startswith('Immune'):
            fac_name = 'Immune'
        else:
            fac_name = 'Infection'
        for i, line in enumerate(lines[1:]):
            info = parse_line(line)
            info['faction'] = fac_name
            info['identity'] = i + 1
            result.append(UnitGroup(**info))

    return result


def parse_line(line):
    import re
    p = r'^(?P<units>\d+)\sunits.+?(?P<hp>\d+)\shit\spoints\s*' \
        + r'(?:\((?P<_special>.+?)\))?\s*' \
        + r'with an attack that does (?P<ap>\d+)\s(?P<dmg_type>\w+)\s*' \
        + r'damage at initiative (?P<initiative>\d+)$'

    m = re.match(p, line)
    info = m.groupdict()
    info['units'] = int(info['units'])
    info['hp'] = int(info['hp'])
    info['ap'] = int(info['ap'])
    info['initiative'] = int(info['initiative'])

    if info['_special'] is not None:
        for seg in info['_special'].split(';'):
            seg = seg.strip()
            pieces = seg.split('to')
            specials = set(x.strip() for x in pieces[1].split(','))
            if pieces[0].startswith('weak'):
                info['weakness'] = specials
            else:
                info['immune'] = specials
    del info['_special']
    return info


def solve_part1(file_path):
    battle = Battle(from_file_data(file_path), 28)
    battle.run()
    print(battle)
    return sum(g.units for g in battle.unit_groups)


def solve_part2(file_path):
    lo_boost = 0
    hi_boost = 5000

    while lo_boost + 1 != hi_boost:
        try_boost = math.floor((lo_boost + hi_boost) / 2)
        print(f'try_boost {try_boost}')
        ug = from_file_data(file_path)
        battle = Battle(ug, try_boost)
        battle.run()
        if not battle.remains('Infection'):
            hi_boost = try_boost
        else:
            lo_boost = try_boost
        print(f'{lo_boost} - {hi_boost}')
        print(battle)

    return sum(g.units for g in battle.unit_groups)
