from io import StringIO
from os import path

testdata = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''


def part1():
    series = []
    for line in read():
        series.append([int(token) for token in line.split(' ')])
    print(sum(s[-1] + predict(s) for s in series))


def part2():
    series = []
    for line in read():
        series.append([int(token) for token in line.split(' ')])
    print(sum(s[0] - predict(s, True) for s in series))


def predict(series, prepend = False):
    done = True
    next = []
    for i in range(len(series) - 1):
        s = series[i + 1] - series[i]
        done = done and s == 0
        next.append(s)
    if done:
        return 0
    return next[0] - predict(next, True) if prepend else next[-1] + predict(next)


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1()
    part2()
