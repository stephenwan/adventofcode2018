from collections import namedtuple
from itertools import takewhile, product


Claim = namedtuple('Claim', 'xl,yl,xh,yh,id')
Segment = namedtuple('Segment', 'l,r,ids')


def solve_part1(input):
    x_segmentation = segmentation(input, 'x')
    y_segmentation = segmentation(input, 'y')

    overlapped = 0
    for xseg, yseg in product(x_segmentation, y_segmentation):
        if len(xseg.ids.intersection(yseg.ids)) > 1:
            overlapped = overlapped + (xseg.r - xseg.l) * (yseg.r - yseg.l)
            print(f'xseg {xseg} yseg {yseg} overlapped {overlapped}')

    return overlapped


def solve_part2(input):
    x_segmentation = segmentation(input, 'x')
    y_segmentation = segmentation(input, 'y')

    ids = set(claim.id for claim in input)
    for xseg, yseg in product(x_segmentation, y_segmentation):
        intersection = xseg.ids.intersection(yseg.ids)
        if len(intersection) > 1:
            ids = ids.difference(intersection)

    return ids


def parse_line(line):
    pieces = line.split(' ')
    id = pieces[0].lstrip('#')
    x, y = pieces[2].rstrip(':').split(',')
    dx, dy = pieces[3].split('x')
    return Claim(int(x), int(y), int(x) + int(dx), int(y) + int(dy), int(id))


def segmentation(input, axis):
    endpointwithrefs = []
    for claim in input:
        endpointwithrefs.append({
            'pos': claim.xl if axis == 'x' else claim.yl,
            'ref': claim
        })
        endpointwithrefs.append({
            'pos': claim.xh if axis == 'x' else claim.yh,
            'ref': None
        })

    endpointwithrefs = sorted(endpointwithrefs,
                              key=lambda s: s['pos'])

    claims = [e['ref'] for e in endpointwithrefs if e['ref'] is not None]

    segments = []
    for left, right in zip(endpointwithrefs, endpointwithrefs[1:]):
        if left['pos'] == right['pos']:
            continue
        segment = Segment(left['pos'], right['pos'], set())
        segments.append(segment)

    idx = 0
    for c in claims:
        while segments[idx].l < (c.xl if axis == 'x' else c.yl):
            idx += 1
        in_claim = (lambda s:
                    s.r <= (c.xh if axis == 'x' else c.yh))
        for segment in takewhile(in_claim, segments[idx:]):
            segment.ids.add(c.id)

    return segments
