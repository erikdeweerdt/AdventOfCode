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
    seeds = []
    maps = {}
    curr = None
    for line in read():
        if line.startswith('seeds: '):
            seeds = [int(s) for s in line[7:].split(' ')]
            continue
        m = re.match(r'(\S+) map:', line)
        if m:
            curr = []
            maps[m.group(1)] = curr
        else:
            curr.append(tuple(int(v) for v in line.split(' ')))
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
    pass

def map_value(v, map):
    for d,s,l in map:
        if v >= s and v < s + l:
            return d + v - s
    return v


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1()
    # part2()
