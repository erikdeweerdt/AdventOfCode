import math
from io import StringIO

testdata = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''


class Cave:
    def __init__(self) -> None:
        self.__bounds = ((500, 0), (500, 0))
        self.__source = (500, 0)
        self.__rock = set()
        self.__sand = set()
        self.__path = [(500, 0)]
        self.grains = 0

    def add_rock(self, path):
        points = iter(path)
        a = next(points)
        for b in points:
            if a[0] == b[0]:
                start = min(a[1], b[1])
                stop = max(a[1], b[1]) + 1
                rocks = ((a[0], y) for y in range(start, stop))
            elif a[1] == b[1]:
                start = min(a[0], b[0])
                stop = max(a[0], b[0]) + 1
                rocks = ((x, a[1]) for x in range(start, stop))
            else:
                raise RuntimeError('Invalid path')
            for rock in rocks:
                self.__extend_bounds(rock)
                self.__rock.add(rock)
            a = b

    def drop_sand(self):
        try:
            while t := self.__next_tile(self.__path[-1]):
                self.__path.append(t)
            self.__sand.add(self.__path.pop())
        except IndexError:
            return False
        self.grains += 1
        return True

    def __next_tile(self, tile):
        x, y = tile
        for t in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
            if not self.__is_in_bounds(t):
                raise IndexError
            if not self.__is_obstructed(t):
                return t
        return None

    def __extend_bounds(self, tile):
        self.__bounds = ((min(self.__bounds[0][0], tile[0]), min(self.__bounds[0][1], tile[1])),
                         (max(self.__bounds[1][0], tile[0]), max(self.__bounds[1][1], tile[1])))

    def __is_in_bounds(self, tile):
        return tile[0] >= self.__bounds[0][0] and tile[0] <= self.__bounds[1][0] and tile[1] >= self.__bounds[0][1] and tile[1] <= self.__bounds[1][1]

    def __is_obstructed(self, tile):
        return tile in self.__rock or tile in self.__sand

    def __str__(self) -> str:
        res = ''
        for y in range(self.__bounds[0][1], self.__bounds[1][1] + 1):
            for x in range(self.__bounds[0][0], self.__bounds[1][0] + 1):
                if (x, y) == self.__source:
                    res += '+'
                elif (x, y) in self.__path:
                    res += '~'
                elif (x, y) in self.__rock:
                    res += '#'
                elif (x, y) in self.__sand:
                    res += 'o'
                else:
                    res += '.'
            res += '\n'
        return res

    def __repr__(self) -> str:
        return str(self)


def part1():
    paths = [[tuple(map(int, point.split(','))) for point in line.split(' -> ')] for line in read()]
    cave = Cave()
    for path in paths:
        cave.add_rock(path)
    while cave.drop_sand():
        pass
    print(cave)
    print(cave.grains)


def part2():
    pass


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1()
    # part2()
