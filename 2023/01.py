import re
from io import StringIO
from os import path

testdata = '''
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''

testdata2 = '''
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''

tokens = ['one', 'two', 'three', 'four',
          'five', 'six', 'seven', 'eight', 'nine']


def part1():
    sum = 0
    for line in read():
        digits = re.findall(r'\d', line)
        sum += int(f'{digits[0]}{digits[-1]}')
    print(sum)


def part2():
    sum = 0
    for line in read():
        digits = re.findall(r'\d', ''.join(
            pop(line[i:]) for i in range(len(line))))
        sum += int(f'{digits[0]}{digits[-1]}')
    print(sum)


def pop(str):
    for j, t in enumerate(tokens):
        if str.startswith(t):
            return f'{j+1}'
    return str[0]


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1()
    part2()
