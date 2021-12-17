import math
import re

# part 1 can be calculated:
# the maximum will be reached when:
# v_x = 0 when the probe hits (then we can freely shift the path up and down)
# y equals the bottom of the target (maximizing the distance to 0, which we must hit due to symmetry)
# plugging that into the formula for adding up all numbers from 0 to n:
# y_max = ((y_min + 1)^2 - (y_min + 1)) / 2 (y_min is given and negative, hence the minus sign, +1 for drag)
# for part 2, the associated velocity (-y_min + 1) is the upper bound because everything higher has its first hit too low

# used for verification of the test target
T = [(int(x), int(y)) for x, y in (l.split(',') for l in re.split(r'\s+', '''
23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
'''.strip()))]


def part1():
    pass


def part2():
    grid = read()
    # max is when the first hit is in the last column
    vx_max = grid[1][0]
    # by solving the quadratic and keeping the positive solution
    vx_min = math.ceil(math.sqrt(1 + 4 * grid[0][0]) / 2 - .5)
    # see part 1
    vy_max = -grid[1][1] - 1
    # min is when shooting down and the first hit is in the bottom row
    vy_min = grid[1][1]
    # print(vx_min, vx_max, vy_min, vy_max)
    # now iterate over all points and see if they hit
    vs = []
    for vx in range(vx_min, vx_max + 1):
        for vy in range(vy_min, vy_max + 1):
            if test(vx, vy, grid):
                vs.append((vx, vy))
    # print(vs)
    print(len(vs))
    # print('-' * 30)
    # for x,y in T:
    #     if (x,y) not in vs:
    #         print(x,y)


def test(vx, vy, grid):
    # if vy > 0, convert to the < 0 case by setting t = 2 * vy + 1 and vy = -vy - 1
    t = 0 if vy <= 0 else 2 * vy + 1
    vy = vy if vy <= 0 else -vy - 1
    # first find possible t's for y (no exceptional case for reaching 0)
    times = []
    y = 0
    while True:
        y += vy
        vy -= 1
        t += 1
        if y < grid[1][1]:
            break
        if y <= grid[0][1]:
            times.append(t)
    # print(times)
    for t in times:
        x = sum(vx - tx for tx in range(min(t, vx + 1)))
        if x >= grid[0][0] and x <= grid[1][0]:
            return True
    return False


def read():
    # don't bother with the file for this one
    # target area: x=20..30, y=-10..-5
    testdata = ((20, -5), (30, -10))
    # target area: x=248..285, y=-85..-56
    data = ((248, -56), (285, -85))
    # return testdata
    return data


if __name__ == '__main__':
    # part1()
    part2()
