
TESTDATA = '2199943210\n3987894921\n9856789892\n8767896789\n9899965678'


def part1():
    with open("data/9.txt") as f:
        grid = [[int(i) for i in l.strip()] for l in f.readlines() if l]
    # grid = [[int(i) for i in l] for l in TESTDATA.splitlines() if l]
    # print(grid)
    mins = find_minima(grid)
    print(mins)
    print(sum(mins) + len(mins))


def part2():
    pass


def find_minima(grid):
    h = len(grid)
    w = len(grid[0])
    mins = []
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if ((y == 0 or c < grid[y - 1][x])
                and (y == h - 1 or c < grid[y + 1][x])
                and (x == 0 or c < grid[y][x - 1])
                    and (x == w - 1 or c < grid[y][x + 1])):
                mins.append(c)
    return mins


if __name__ == '__main__':
    part1()
    part2()
