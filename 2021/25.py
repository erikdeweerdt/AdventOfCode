from itertools import product


class Grid:
    def __init__(self, data):
        self.__w = len(data[0])
        self.__h = len(data)
        self.__grid = {
            (x, y): data[y][x]
            for x, y in product(range(self.__w), range(self.__h))
            if data[y][x] != '.'
        }

    def __str__(self):
        return '\n'.join(''.join(self.__grid.get((x, y), '.') for x in range(self.__w)) for y in range(self.__h))

    def move(self, east):
        token = '>' if east else 'v'
        grid = {}
        count = 0
        for p, v in self.__grid.items():
            if v == token:
                np = ((p[0] + 1) % self.__w, p[1]) if east else (p[0], (p[1] + 1) % self.__h)
                if np in self.__grid:
                    grid[p] = v
                else:
                    grid[np] = v
                    count += 1
            else:
                grid[p] = v
        self.__grid = grid
        return count


def part1():
    grid = read()
    print(grid)
    step = 1
    # don't use 'or' below: short-circuiting will prevent the second move
    while grid.move(True) + grid.move(False) > 0:
        step += 1
    print(step)
    print(grid)


def part2():
    # no part 2!
    pass


def read():
    with open('data/25.txt') as f:
        data = list(map(str.strip, f.readlines()))
    return Grid(data)


if __name__ == '__main__':
    part1()
    part2()
