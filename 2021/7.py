import statistics


def part1():
    with open("data/7.txt") as f:
        data = [int(l) for l in f.readline().split(',')]
    # the median minimizes the total distance
    # see https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm
    m = statistics.median(data)
    # the fuel amount is asked
    f = sum((abs(i - m) for i in data))
    print(m, f)


def part2():
    with open("data/7.txt") as f:
        data = [int(l) for l in f.readline().split(',')]
    # data = [16,1,2,0,4,2,7,1,2,14]
    # total fuel consumption to move n spaces: 1 + 2 + 3 + ... + n = (n^2 + n) / 2
    # just brute force it; the data set is small enough
    # not sure if an analytical solution exists (note that the average is close enough to work "by luck")
    # it may be possible to optimize the search a bit, though (convex function with 1 global minimum)
    fuel = list((sum(((abs(i - r) ** 2 + abs(i - r))/2 for i in data)) for r in range(1000)))
    print(min(fuel))


if __name__ == '__main__':
    # part1()
    part2()
