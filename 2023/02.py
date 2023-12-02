import re
from io import StringIO
from os import path

testdata = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''


def part1():
    cubes = (12, 13, 14)
    sum = 0
    for line in read():
        id, game = re.findall(r'Game (\d+): (.*)', line)[0]
        possible = all(cmp(round(r), cubes) for r in game.split('; '))
        print(f'{id}: {possible}')
        if (possible):
            sum += int(id)
    print(sum)


def part2():
    sum = 0
    for line in read():
        id, game = re.findall(r'Game (\d+): (.*)', line)[0]
        pwr = power(list(round(r) for r in game.split('; ')))
        print(f'{id}: {pwr}')
        sum += pwr
        # if (possible):
        #     sum += int(id)
    print(sum)


def round(str):
    r, g, b = 0, 0, 0
    for count, color in re.findall(r'(\d+) (red|green|blue)', str):
        if color == 'red':
            r += int(count)
        elif color == 'green':
            g += int(count)
        elif color == 'blue':
            b += int(count)
    return r, g, b


def cmp(a, b, cond=lambda a, b: a <= b):
    for i in range(len(a)):
        if not cond(a[i], b[i]):
            return False
    return True


def power(game):
    r = max(rnd[0] for rnd in game)
    g = max(rnd[1] for rnd in game)
    b = max(rnd[2] for rnd in game)
    return r*g*b


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
