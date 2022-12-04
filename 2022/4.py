import regex

testdata = '''
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''


def part1():
    count = 0
    for (a, b), (c, d) in read():
        if a == c:
            # if a == c, the longest range always contains the shorter one
            count += 1
        elif a < c:
            count += 1 if b >= d else 0
        else:
            count += 1 if b <= d else 0
    print(count)


def part2():
    count = 0
    for (a, b), (c, d) in read():
        if a == c:
            count += 1
        elif a < c:
            count += 1 if b >= c else 0
        else:
            count += 1 if a <= d else 0
    print(count)


def read():
    with open(f'data/{__file__.replace(".py", ".txt")}') as f:
        data = list(map(str.strip, f.readlines()))
    # data = list(map(str.strip, testdata.splitlines()))
    for line in data:
        if line:
            r = list(map(int, regex.split('[,-]', line)))
            yield ((r[0], r[1]), (r[2], r[3]))


if __name__ == '__main__':
    # part1()
    part2()
