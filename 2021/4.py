import re

SIZE = 5


class Grid:
    def __init__(self):
        self.__grid = []
        self.__rows = [SIZE for _ in range(SIZE)]
        self.__cols = [SIZE for _ in range(SIZE)]

    def __str__(self):
        return '\n'.join((' '.join((f'{x: >2}' for x in row)) for row in self.__grid))

    def add_row(self, row):
        self.__grid.append([int(x) for x in re.split(r' +', row)])

    def mark(self, number):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.__grid[r][c] == number:
                    self.__grid[r][c] = -1
                    self.__rows[r] -= 1
                    self.__cols[c] -= 1
                    return self.__rows[r] == 0 or self.__cols[c] == 0

    def score(self, number):
        score = 0
        for r in range(SIZE):
            for c in range(SIZE):
                if self.__grid[r][c] >= 0:
                    score += self.__grid[r][c]
        return score * number


def part1():
    with open("data/4.txt") as f:
        data = [l.strip() for l in f.readlines()]
    numbers = [int(x) for x in data[0].split(',')]
    grids = make_grids(data[1:])
    print(bingo(numbers, grids))


def part2():
    with open("data/4.txt") as f:
        data = [l.strip() for l in f.readlines()]
    numbers = [int(x) for x in data[0].split(',')]
    grids = make_grids(data[1:])
    print(bingo_last(numbers, grids))


def make_grids(data):
    grids = []
    g = None
    for l in data[1:]:
        if l:
            if not g:
                g = Grid()
            g.add_row(l)
        elif g:
            grids.append(g)
            g = None
    return grids


def bingo(numbers, grids):
    for n in numbers:
        for g in grids:
            if g.mark(n):
                return g.score(n)

def bingo_last(numbers, grids):
    last = None
    last_turns = 0
    last_num = 0
    for g in grids:
        t = 0
        for n in numbers:
            t += 1
            if g.mark(n):
                if t > last_turns:
                    last = g
                    last_turns = t
                    last_num = n
                break
    return last.score(last_num)


if __name__ == '__main__':
    # part1()
    part2()
