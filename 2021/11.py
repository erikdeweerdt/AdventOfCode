TESTDATA = [
    '5483143223',
    '2745854711',
    '5264556173',
    '6141336146',
    '6357385478',
    '4167524645',
    '2176841721',
    '6882881134',
    '4846848554',
    '5283751526',
]


def part1():
    with open("data/11.txt") as f:
        grid = [[int(c) for c in l.strip()] for l in f.readlines() if l]
    # grid = [[int(c) for c in l] for l in TESTDATA]
    count = 0
    for _ in range(100):
        # print_grid(grid)
        # print('-' * 19)
        # increase all by 1 and enqueue all > 9
        q = []
        for y in range(10):
            for x in range(10):
                grid[y][x] += 1
                if grid[y][x] > 9:
                    q.append((x, y))
        # process flashers
        flashes = []
        while q:
            qx, qy = q.pop(0)
            flashes.append((qx, qy))
            for nx, ny in neighbors(qx, qy):
                if grid[ny][nx] <= 9:
                    grid[ny][nx] += 1
                    if grid[ny][nx] > 9:
                        q.append((nx, ny))
        # count and reset
        # print(flashes)
        count += len(flashes)
        for x, y in flashes:
            grid[y][x] = 0
    print(count)


def part2():
    with open("data/11.txt") as f:
        grid = [[int(c) for c in l.strip()] for l in f.readlines() if l]
    # grid = [[int(c) for c in l] for l in TESTDATA]
    count = 0
    i = 0
    while True:
        i += 1
        # print_grid(grid)
        # print('-' * 19)
        # increase all by 1 and enqueue all > 9
        q = []
        for y in range(10):
            for x in range(10):
                grid[y][x] += 1
                if grid[y][x] > 9:
                    q.append((x, y))
        # process flashers
        flashes = []
        while q:
            qx, qy = q.pop(0)
            flashes.append((qx, qy))
            for nx, ny in neighbors(qx, qy):
                if grid[ny][nx] <= 9:
                    grid[ny][nx] += 1
                    if grid[ny][nx] > 9:
                        q.append((nx, ny))
        # count and reset
        # print(flashes)
        if len(flashes) == 100:
            print(i)
            break
        count += len(flashes)
        for x, y in flashes:
            grid[y][x] = 0
    # print(count)


def print_grid(grid):
    print('\n'.join(' '.join(str(c) for c in l) for l in grid))


def neighbors(x, y):
    for nx in range(x - 1, x + 2, 1):
        for ny in range(y - 1, y + 2, 1):
            if nx >= 0 and nx < 10 and ny >= 0 and ny < 10:
                yield (nx, ny)


if __name__ == '__main__':
    # part1()
    part2()
