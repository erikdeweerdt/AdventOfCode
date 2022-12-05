import re
from io import StringIO

testdata = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''


def move(stacks, movement):
    count, src, dst = movement
    for _ in range(count):
        stacks[dst].insert(0, stacks[src].pop(0))


def move_substack(stacks, movement):
    count, src, dst = movement
    for i in range(count):
        stacks[dst].insert(i, stacks[src].pop(0))


def part1():
    stacks, movements = read()
    for movement in movements:
        move(stacks, movement)
    print(''.join([s[0] for s in stacks]))


def part2():
    stacks, movements = read()
    for movement in movements:
        move_substack(stacks, movement)
    print(''.join([s[0] for s in stacks]))


def read_stacks(f):
    stacks = None
    while line := f.readline():
        if line.startswith(' 1'):
            break
        if line.strip():
            if stacks is None:
                stacks = [[] for _ in range(len(line) // 4)]
            for i in range(0, len(line), 4):
                token = line[i+1:i+2]
                if token != ' ':
                    stacks[i//4].append(token)
    return stacks


def read_movements(f):
    pattern = re.compile(r'^move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)$')
    while line := f.readline():
        if match := pattern.match(line):
            yield (int(match.group('count')), int(match.group('from')) - 1, int(match.group('to')) - 1)


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        stacks = read_stacks(f)
        movements = list(read_movements(f))
    return stacks, movements


if __name__ == '__main__':
    part1()
    part2()
