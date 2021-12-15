TESTDATA = [
    '1163751742',
    '1381373672',
    '2136511328',
    '3694931569',
    '7463417111',
    '1319128137',
    '1359912421',
    '3125421639',
    '1293138521',
    '2311944581',
]


def part1():
    grid = read()
    print(findpath(grid, len(grid[0]), len(grid)))


def part2():
    # same as part 1, but with a tiled map
    grid = read()
    print(findpath(grid, len(grid[0]) * 5, len(grid) * 5))


def findpath(grid, w, h):
    risk = [[float('inf') for _ in range(w)] for _ in range(h)]
    risk[0][0] = 0
    q = [(0, 0)]
    while q:
        qx, qy = q.pop(0)
        r = risk[qy][qx]
        for nx, ny in neighbors(qx, qy, w, h):
            nr = r + get(grid, nx, ny)
            if nr < risk[ny][nx]:
                risk[ny][nx] = nr
                q.append((nx, ny))
    # print(risk)
    return risk[-1][-1]


def get(grid, x, y):
    # avoid the need of precalculating the whole grid
    w = len(grid[0])
    h = len(grid)
    # value + 1 for every next tile in any direction
    v = grid[y % h][x % w] + x // w + y // h
    # can't use mod because it wraps around to 1 instead of 0
    # breaks if the maximum change exceeds 10 (it's 8 for 5 tiles in both directions)
    return v if v < 10 else v - 9


def neighbors(x, y, w, h):
    for nx in range(x - 1, x + 2, 1):
        for ny in range(y - 1, y + 2, 1):
            # exclude diagonal
            if nx == x or ny == y:
                if nx >= 0 and nx < w and ny >= 0 and ny < h:
                    yield (nx, ny)


def read():
    with open("data/15.txt") as f:
        grid = [[int(c) for c in l.strip()] for l in f.readlines() if l.strip()]
    # grid = [[int(c) for c in l] for l in TESTDATA]
    return grid


if __name__ == '__main__':
    # part1()
    part2()
