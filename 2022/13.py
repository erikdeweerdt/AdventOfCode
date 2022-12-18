from functools import cmp_to_key
from io import StringIO
from itertools import zip_longest
from typing import Optional

import regex

testdata = '''
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''


def compare(left, right) -> int:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return -1
            if left > right:
                return 1
            return 0
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    for l, r in zip_longest(left, right):
        if l is None:
            return -1
        if r is None:
            return 1
        decision = compare(l, r)
        if decision != 0:
            return decision
    return 0


def parse(iterable):
    while True:
        token = next(iterable)
        if token == '[':
            yield list(parse(iterable))
        elif token == ']':
            break
        else:
            yield int(token)


def part1():
    packets = read()
    index = 0
    total = 0
    for left in packets:
        right = next(packets)
        index += 1
        if compare(left, right) < 0:
            total += index
    print(total)


def part2():
    div1 = [[2]]
    div2 = [[6]]
    packets = [div1, div2] + list(read())
    index = 0
    for packet in sorted(packets, key=cmp_to_key(compare)):
        index += 1
        if packet == div1:
            d1 = index
        elif packet == div2:
            d2 = index
    print(div1, d1)
    print(div2, d2)
    print(d1*d2)


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                r = regex.findall(r'(\[|]|\d+)', line)
                yield next(parse(iter(r)))


if __name__ == '__main__':
    # part1()  # 5684
    part2()
