import re
from functools import reduce
from io import StringIO
from math import lcm
from os import path

testdata = '''
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''
testdata2 = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''

def part1():
    global path, nodes
    path, nodes = parse()
    node = 'AAA'
    count = 0
    i = 0
    while node != 'ZZZ':
        node = nodes[node][path[i]]
        count += 1
        i = (i + 1) % len(path)
    print(count)


def part2():
    global path, nodes
    path, nodes = parse()
    # brute forcing this, even with caching to detect cycles, isn't going to cut it
    # printing intermediate results revealed that the ghosts only execute perfect cycles, i.e. consume the entire path and end up on the same node again _in the same number of steps_
    # -> the answer is the lcm of all path lengths after just one iteration
    # THIS IS NOT A GENERAL SOLUTION AND ONLY WORKS BECAUSE OF THE SPECIFIC INPUT
    ghosts = [nextZ(n,0)[2] for n in nodes.keys() if n.endswith('A')]
    print(reduce(lcm, ghosts))

def nextZ(node, i):
    count = 0
    while count == 0 or not node.endswith('Z'):
        node = nodes[node][path[i]]
        count += 1
        i = (i + 1) % len(path)
    return node, i, count

def parse(data=None):
    path = None
    nodes = {}
    for line in read(data):
        if not path:
            path = [0 if p == 'L' else 1 for p in line]
        elif m := re.match(r'(.{3}) = \((.{3}), (.{3})\)', line):
            nodes[m.group(1)] = (m.group(2), m.group(3))
    return path, nodes


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
