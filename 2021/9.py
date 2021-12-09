
TESTDATA = '2199943210\n3987894921\n9856789892\n8767896789\n9899965678'


def part1():
    with open("data/9.txt") as f:
        grid = [[int(i) for i in l.strip()] for l in f.readlines() if l]
    # grid = [[int(i) for i in l] for l in TESTDATA.splitlines() if l]
    # print(grid)
    mins = find_minima(grid)
    # print(mins)
    print(sum(grid[y][x] for x, y in mins) + len(mins))


def part2():
    with open("data/9.txt") as f:
        grid = [[int(i) for i in l.strip()] for l in f.readlines() if l]
    # grid = [[int(i) for i in l] for l in TESTDATA.splitlines() if l]
    mins = find_minima(grid)
    # print(mins)
    basins = flood_fill(grid, mins)
    # print(basins)
    sizes = sorted((s for x, y, s in basins), reverse=True)
    print(sizes[0]*sizes[1]*sizes[2])


def find_minima(grid):
    h = len(grid)
    w = len(grid[0])
    mins = []
    for y in range(h):
        for x in range(w):
            c = grid[y][x]
            if any((grid[ny][nx] <= c for nx, ny in neighbors(w, h, x, y))):
                continue
            mins.append((x, y))
    return mins


def flood_fill(grid, mins):
    # finding the basins is a flood fill
    # this can be implemented with a breadth-first search
    h = len(grid)
    w = len(grid[0])
    basins = []
    for x, y in mins:
        q = [(x, y)]
        s = 0
        while q:
            qx, qy = q.pop(0)
            # point may have been processed via another path already
            if grid[qy][qx] >= 0:
                s += 1
                grid[qy][qx] = -1
                for nx, ny in neighbors(w, h, qx, qy):
                    if grid[ny][nx] < 9 and grid[ny][nx] >= 0:
                        q.append((nx, ny))
        basins.append((x, y, s))
        # print('\n'.join(''.join(str(c) if c >= 0 else '.' for c in l) for l in grid))
        # print(f'---------------> {s}')
    return basins


def neighbors(w, h, x, y):
    if x > 0:
        yield (x-1, y)
    if x < w - 1:
        yield (x+1, y)
    if y > 0:
        yield (x, y-1)
    if y < h - 1:
        yield (x, y+1)


if __name__ == '__main__':
    # part1()
    part2()
