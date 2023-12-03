import re
from io import StringIO
from os import path

testdata = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''


def part1():
    nums = []
    syms = []
    row = 0
    for line in read():
        for m in re.finditer(r'[0-9]+|[^0-9.]', line):
            val = m.group()
            pos = (row, m.start())
            try:
                nums.append((int(val), pos))
            except ValueError:
                syms.append((val, pos))
        row += 1
    # print(nums)
    # print(syms)
    print(sum(num[0] for num in nums if is_part(num, syms)))


def part2():
    nums = []
    syms = []
    row = 0
    for line in read():
        for m in re.finditer(r'[0-9]+|[^0-9.]', line):
            val = m.group()
            pos = (row, m.start())
            try:
                nums.append((int(val), pos))
            except ValueError:
                if val == '*':
                    syms.append((val, pos))
        row += 1
    # print(nums)
    # print(syms)
    print(sum(gear_ratio(s, nums) for s in syms))


def is_part(num, syms):
    n, (nr, nc) = num
    for _, (sr, sc) in syms:
        if sr >= nr - 1 and sr <= nr + 1 and sc >= nc - 1 and sc <= nc + len(str(n)):
            return True
    return False


def gear_ratio(sym, nums):
    parts = []
    _, (sr, sc) = sym
    for n, (nr, nc) in nums:
        if sr >= nr - 1 and sr <= nr + 1 and sc >= nc - 1 and sc <= nc + len(str(n)):
            parts.append(n)
    if len(parts) == 2:
        return parts[0] * parts[1]
    return 0


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
