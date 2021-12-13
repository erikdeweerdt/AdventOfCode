TESTDATA = [
    '6,10',
    '0,14',
    '9,10',
    '0,3',
    '10,4',
    '4,11',
    '6,0',
    '6,12',
    '4,1',
    '0,13',
    '10,12',
    '3,4',
    '3,0',
    '8,4',
    '1,10',
    '2,14',
    '8,10',
    '9,0',
    '',
    'fold along y=7',
    'fold along x=5',
]


class Grid:
    def __init__(self) -> None:
        self.__grid = set()

    def __str__(self):
        sx = max(p[0] for p in self.__grid) + 1
        sy = max(p[1] for p in self.__grid) + 1
        return '\n'.join(' '.join('#' if (x, y) in self.__grid else '.' for x in range(sx)) for y in range(sy))

    def add(self, x, y):
        self.__grid.add((x, y))

    def fold(self, fold):
        # partition left-right and merge
        axis, value = fold
        grid = set()
        for p in self.__grid:
            # immediately merge in points to the right
            # no points are on the fold, so ignore that case
            if p[axis] < value:
                grid.add(p)
            else:
                np = list(p)
                np[axis] = 2 * value - np[axis]
                grid.add(tuple(np))
        self.__grid = grid

    def count_dots(self):
        return len(self.__grid)


def part1():
    grid, folds = read()
    grid.fold(folds[0])
    print(grid.count_dots())


def part2():
    grid, folds = read()
    for f in folds:
        grid.fold(f)
    print(grid)


def read():
    with open("data/13.txt") as f:
        data = [l.strip() for l in f.readlines() if l.strip()]
    # data = [l.strip() for l in TESTDATA if l]
    grid = Grid()
    folds = []
    for l in data:
        if l.startswith('fold along '):
            # x-axis = 0, y-axis = 1
            folds.append((0 if l[11] == 'x' else 1, int(l[13:])))
        else:
            x, y = l.split(',')
            grid.add(int(x), int(y))
    return grid, folds


if __name__ == '__main__':
    part1()
    part2()
