import re

PATTERN = re.compile(r'^(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)')


class Line:
    def __init__(self, repr):
        m = PATTERN.search(repr)
        if m:
            self.__x1 = int(m.group('x1'))
            self.__y1 = int(m.group('y1'))
            self.__x2 = int(m.group('x2'))
            self.__y2 = int(m.group('y2'))
        else:
            raise ValueError()

    def is_diagonal(self):
        return self.__x1 != self.__x2 and self.__y1 != self.__y2

    def max(self):
        return max(self.__x1, self.__x2, self.__y1, self.__y2)

    def points(self):
        # lines are either horizontal, vertical or 45 degrees
        dx = Line.delta(self.__x1, self.__x2)
        dy = Line.delta(self.__y1, self.__y2)
        x = self.__x1
        y = self.__y1
        while x != self.__x2 or y != self.__y2:
            yield x, y
            x += dx
            y += dy
        # end point
        yield x, y

    @staticmethod
    def delta(a, b):
        if a == b:
            return 0
        return 1 if a < b else -1


class Grid:
    def __init__(self, size):
        self.__size = size
        self.__grid = [[0 for _ in range(size)] for _ in range(size)]

    def mark(self, line):
        for x, y in line.points():
            self.__grid[x][y] += 1

    def overlap_count(self):
        count = 0
        for x in range(self.__size):
            for y in range(self.__size):
                if self.__grid[x][y] > 1:
                    count += 1
        return count


def count_overlaps(include_diagonal):
    with open("data/5.txt") as f:
        lines = [Line(l) for l in f.readlines() if l]
    size = max((l.max() for l in lines)) + 1
    grid = Grid(size)
    for line in lines:
        if include_diagonal or not line.is_diagonal():
            grid.mark(line)
    return grid.overlap_count()


def part1():
    print(count_overlaps(False))


def part2():
    print(count_overlaps(True))


if __name__ == '__main__':
    part1()
    part2()
