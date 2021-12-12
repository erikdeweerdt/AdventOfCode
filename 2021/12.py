TESTDATA = [
    'start-A',
    'start-b',
    'A-c',
    'A-b',
    'b-d',
    'A-end',
    'b-end',
]
TESTDATA2 = [
    'fs-end',
    'he-DX',
    'fs-he',
    'start-DX',
    'pj-DX',
    'end-zg',
    'zg-sl',
    'zg-pj',
    'pj-he',
    'RW-he',
    'fs-DX',
    'pj-RW',
    'zg-RW',
    'start-pj',
    'he-WI',
    'zg-he',
    'pj-fs',
    'start-RW',
]


class CaveSystem:
    def __init__(self):
        self.__system = {}

    def __str__(self) -> str:
        return str(self.__system)

    def add(self, a, b):
        if a in self.__system:
            self.__system[a].add(b)
        else:
            self.__system[a] = {b}

    def paths(self, start='start', path=[], visited={'start'}):
        # assume no loops
        # print(start,path,visited)
        if start == 'end':
            yield path + [start]
        else:
            for cave in self.__system[start]:
                v = set(visited)
                if cave.islower():
                    if cave in v:
                        continue
                    v.add(cave)
                yield from self.paths(cave, path + [start], v)


def part1():
    with open("data/12.txt") as f:
        data = [l.strip().split('-') for l in f.readlines() if l]
    # data = (l.split('-') for l in TESTDATA2)
    system = CaveSystem()
    for a, b in data:
        # connections are one-directional, so add both
        system.add(a, b)
        system.add(b, a)
    # print(system)
    count = 0
    for p in system.paths():
        count += 1
        print(p)
    print(count)


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
