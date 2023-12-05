import re
from io import StringIO
from math import inf
from os import path

testdata = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''


def part1():
    seeds, maps = parse()
    # print(seeds)
    # print(maps)
    min_value = inf
    for s in seeds:
        # print(f'----------\nseed: {s}')
        # dicts preserver insertion order
        v = s
        for name, map in maps.items():
            v = map_value(v, map)
            # print(f'{name}: {v}')
        if v < min_value:
            min_value = v
    print(min_value)

def part2():
    seeds, maps = parse()
    ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    for name, map in maps.items():
        new_ranges = []
        for r in ranges:
            new_ranges += map_range(r, map)
        ranges = new_ranges
        # print(name)
        # print(ranges)
    print(min(r[0] for r in ranges))
    # print(map_range(ranges[1], maps['seed-to-soil']))

def map_value(v, map):
    for d,s,l in map:
        if v >= s and v < s + l:
            return d + v - s
    return v

# nasty code is nasty
# works by mapping pieces of the source range and filling the holes afterwards
# makes part 2 run in 20ms
def map_range(r, map):
    rs,rl = r
    ranges = []
    for d,s,l in map:
        a = max(rs, s)
        b = min(rs + rl, s + l)
        if a < b:
            ranges.append((a, b - a, d - s))
    ranges.sort(key=lambda r: r[0])
    if len(ranges) == 0:
        return [r]
    # plug holes
    plugged = [ranges[0]]
    for i in range(1, len(ranges)):
        ps,pl,_ = plugged[-1]
        s,_,_ = ranges[i]
        if ps + pl < s:
            plugged.append((ps + pl, s - (ps + pl), 0))
        plugged.append(ranges[i])
    # front and back
    if plugged[0][0] > rs:
        plugged.insert(0, (rs, plugged[0][0] - rs, 0))
    end = plugged[-1][0] + plugged[-1][1]
    if end < rs + rl:
        plugged.append((end, rs + rl - end, 0))
    return [(p[2] + p[0], p[1]) for p in plugged]


def parse(data=None):
    seeds = []
    maps = {}
    curr = None
    for line in read(data):
        if line.startswith('seeds: '):
            seeds = [int(s) for s in line[7:].split(' ')]
            continue
        m = re.match(r'(\S+) map:', line)
        if m:
            curr = []
            maps[m.group(1)] = curr
        else:
            curr.append(tuple(int(v) for v in line.split(' ')))
    return seeds, maps


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
