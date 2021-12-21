def part1():
    # loser, rolls = deterministic(4, 8)
    loser, rolls = deterministic(5, 9)
    print(loser, rolls, loser * rolls)


def part2():
    pass


def quantum(player1, player2):
    # still roll 3 times
    # -> every turn yields a sum of at least 3 and at most 9 (normally distributed)
    pass


def deterministic(player1, player2):
    p1 = player1 - 1
    p2 = player2 - 1
    s1 = 0
    s2 = 0
    die = 0
    rolls = 0
    while True:
        die, s = roll(die)
        rolls += 3
        p1 = (p1 + s) % 10
        s1 += p1 + 1
        if s1 >= 1000:
            # score of the losing player is needed
            return s2, rolls
        die, s = roll(die)
        rolls += 3
        p2 = (p2 + s) % 10
        s2 += p2 + 1
        if s2 >= 1000:
            # score of the losing player is needed
            return s1, rolls


def roll(die):
    s = 3 * die + 3
    nd = (die + 3) % 100
    if nd < die:
        s -= 100 * (nd + 1)
    return nd, s + 3


if __name__ == '__main__':
    part1()
    part2()
