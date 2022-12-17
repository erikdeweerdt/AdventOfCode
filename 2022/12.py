import math
from io import StringIO
from typing import List, Tuple

testdata = '''
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''


class Node:
    height: int
    distance: float = math.inf
    is_start: bool = False
    is_end: bool = False
    is_bottom: bool

    def __init__(self, height) -> None:
        if height == 'S':
            self.is_start = True
            height = 'a'
        elif height == 'E':
            self.is_end = True
            height = 'z'
        self.height = ord(height)
        self.is_bottom = height == 'a'

    def can_move(self, node):
        return node.height <= self.height + 1


class HeightMap:
    __grid: List[List[Node]]
    __size: Tuple[int, int]
    __start: Tuple[int, int]
    __end: Tuple[int, int]

    def __init__(self) -> None:
        self.__grid = []

    def reset(self):
        for row in self.__grid:
            for node in row:
                node.distance = math.inf

    def all_starting_points(self):
        for y, row in enumerate(self.__grid):
            for x, node in enumerate(row):
                if node.is_bottom:
                    yield (x, y)

    def add_row(self, data):
        row: List[Node] = []
        y = len(self.__grid)
        for x, char in enumerate(data):
            node = Node(char)
            if node.is_start:
                self.__start = (x, y)
            elif node.is_end:
                self.__end = (x, y)
            row.append(node)
        self.__grid.append(row)
        self.__size = (len(row), len(self.__grid))

    def neighbors(self, n):
        x, y = n
        if x > 0:
            yield (x-1, y)
        if x < self.__size[0] - 1:
            yield(x+1, y)
        if y > 0:
            yield(x, y-1)
        if y < self.__size[1] - 1:
            yield(x, y+1)

    def get_node(self, n):
        return self.__grid[n[1]][n[0]]

    def find_route(self, start=None):
        queue: List[Tuple[int, int]] = [start if start is not None else self.__start]
        self.get_node(queue[0]).distance = 0
        while True:
            try:
                c = queue.pop(0)
            except IndexError:
                break
            if c == self.__end:
                break
            node = self.get_node(c)
            d = node.distance + 1
            dirty = False
            for n in self.neighbors(c):
                neighbor = self.get_node(n)
                if node.can_move(neighbor) and d < neighbor.distance:
                    dirty = True
                    neighbor.distance = d
                    if n not in queue:
                        queue.append(n)
            if dirty:
                queue.sort(key=lambda k: self.get_node(k).distance)
        return self.get_node(self.__end).distance


def part1():
    height_map = HeightMap()
    for line in read():
        height_map.add_row(line)
    print(height_map.find_route())


def part2():
    height_map = HeightMap()
    for line in read():
        height_map.add_row(line)
    shortest = math.inf
    for starting_point in height_map.all_starting_points():
        height_map.reset()
        shortest = min(shortest, height_map.find_route(starting_point))
    print(shortest)


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()  # 423
    part2()  # 416
