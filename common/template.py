from io import StringIO

testdata = '''
'''


def part1():
    pass


def part2():
    pass


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1()
    # part2()
