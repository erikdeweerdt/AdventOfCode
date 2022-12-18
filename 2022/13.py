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


def in_order(left, right) -> Optional[bool]:
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            if left > right:
                return False
            return None
        return in_order([left], right)
    if isinstance(right, int):
        return in_order(left, [right])
    for l, r in zip_longest(left, right):
        if l is None:
            return True
        if r is None:
            return False
        decision = in_order(l, r)
        if decision is not None:
            return decision


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
        if in_order(left, right):
            total += index
    print(total)


def part2():
    pass


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                r = regex.findall(r'(\[|]|\d+)', line)
                yield next(parse(iter(r)))


if __name__ == '__main__':
    part1()  # 5684
    # part2()
