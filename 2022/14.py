import math
from copy import deepcopy
from io import StringIO

testdata = '''
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''


class Cave:
    def __init__(self, min_x, max_x, depth) -> None:
        self.__min_x = min_x
        self.__max_x = max_x
        self.__width = max_x - min_x + 1
        self.__height = depth
        self.__cave = [['.' for _ in range(self.__width)] for _ in range(self.__height)]
        self.__cave[0][500 - self.__min_x] = '+'
        self.__path = [(500 - self.__min_x, 0)]
        self.grains = 0

    # def translate_coord(self, c):
    #     return (c[0] - self.__min_x, c[1])

    def add_path(self, path):
        points = iter(path)
        a = next(points)
        for b in points:
            if a[0] == b[0]:
                self.__vertical_path(a[0], a[1], b[1])
            elif a[1] == b[1]:
                self.__horizontal_path(a[1], a[0], b[0])
            else:
                raise RuntimeError('Invalid path')
            a = b

    def drop_sand(self):
        try:
            while t := self.__next_tile(self.__path[-1]):
                if t[0] < 0:
                    raise IndexError
                self.__path.append(t)
            x, y = self.__path.pop()
            self.__cave[y][x] = 'o'
        except IndexError:
            return False
        self.grains += 1
        return True

    def __next_tile(self, tile):
        x, y = tile
        if self.__cave[y + 1][x] == '.':
            return (x, y + 1)
        if self.__cave[y + 1][x - 1] == '.':
            return (x - 1, y + 1)
        if self.__cave[y + 1][x + 1] == '.':
            return (x + 1, y + 1)
        return None

    def __horizontal_path(self, y, a, b):
        if a < b:
            start = a - self.__min_x
            end = b - self.__min_x + 1
        else:
            start = b - self.__min_x
            end = a - self.__min_x + 1
        for x in range(start, end):
            self.__cave[y][x] = '#'

    def __vertical_path(self, x, a, b):
        if a < b:
            start = a
            end = b
        else:
            start = b
            end = a
        x -= self.__min_x
        for y in range(start, end):
            self.__cave[y][x] = '#'

    def __str__(self) -> str:
        cave = deepcopy(self.__cave)
        for x, y in self.__path[1:]:
            cave[y][x] = '~'
        return '\n'.join(''.join(row) for row in cave)

    def __repr__(self) -> str:
        return str(self)


def part1():
    paths = [[tuple(map(int, point.split(','))) for point in line.split(' -> ')] for line in read()]
    min_x = math.inf
    max_x = -math.inf
    depth = 0
    for path in paths:
        for point in path:
            min_x = min(min_x, point[0])
            max_x = max(max_x, point[0])
            depth = max(depth, point[1])
    cave = Cave(min_x, max_x, depth + 1)
    for path in paths:
        cave.add_path(path)
    # print(cave)
    while cave.drop_sand():
        # print()
        # print(cave)
        pass
    # print()
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
