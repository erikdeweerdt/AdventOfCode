from functools import reduce

testdata = [
    ['A', 'Y'],
    ['B', 'X'],
    ['C', 'Z'],
]

opponent_map = {'A': 'R', 'B': 'P', 'C': 'S'}
you_map = {'X': 'R', 'Y': 'P', 'Z': 'S'}
scores_map = {'R': 1, 'P': 2, 'S': 3}
win_map = {'R': 'S', 'P': 'R', 'S': 'P'}
lose_map = {v: k for k, v in win_map.items()}


def score(opponent, you):
    o = opponent_map[opponent]
    y = you_map[you]
    s = scores_map[y]
    if o == y:
        s += 3
    else:
        s += 6 if win_map[y] == o else 0
    return s


def strategy_score(opponent, you):
    o = opponent_map[opponent]
    if you == 'X':
        # note: you lose, so y must be whatever o wins from
        y = win_map[o]
        s = scores_map[y]
    elif you == 'Y':
        y = o
        s = 3 + scores_map[y]
    else:
        y = lose_map[o]
        s = 6 + scores_map[y]
    return s


def part1():
    total = reduce(lambda t, g: t + score(g[0], g[1]), read(), 0)
    print(total)


def part2():
    total = reduce(lambda t, g: t + strategy_score(g[0], g[1]), read(), 0)
    print(total)


def read():
    with open('data/2.txt') as f:
        data = list(map(str.strip, f.readlines()))
    for line in data:
        if line:
            yield line.split()


if __name__ == '__main__':
    part1()
    part2()
