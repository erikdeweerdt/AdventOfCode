import re
from io import StringIO
from os import path

testdata = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''


def part1():
    s = 0
    for line in read():
        _, winning, yours = re.split(r':\s+|\s+\|\s+', line)
        winning = set(int(w) for w in re.split(r'\s+', winning))
        yours = set(int(y) for y in re.split(r'\s+', yours))
        l = len(winning.intersection(yours)) - 1
        s += 2 ** l if l >= 0 else 0
    print(s)


def part2():
    s = 0
    copies = []
    for line in read():
        _, winning, yours = re.split(r':\s+|\s+\|\s+', line)
        winning = set(int(w) for w in re.split(r'\s+', winning))
        yours = set(int(y) for y in re.split(r'\s+', yours))
        l = len(winning.intersection(yours))
        c = copies.pop(0) if len(copies) else 1
        s += c
        if l:
            copies = [copies[i] + c if i < len(copies) else 1 + c for i in range(l)] + copies[l:]
    print(s)


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
