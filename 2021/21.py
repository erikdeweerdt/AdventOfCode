from functools import reduce

PROBABILITIES = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]


def part1():
    # loser, rolls = deterministic(4, 8)
    loser, rolls = deterministic(5, 9)
    print(loser, rolls, loser * rolls)


def part2():
    # print(quantum(4 - 1, 8 - 1))
    print(quantum(5 - 1, 9 - 1))


# turn = True if player1 is playing
# there may be a more clever way of doing this, but I don't care
def quantum(p1, p2, s1=0, s2=0, u=1, turn=True):
    if turn:
        if s2 >= 21:
            return (0, u)
        u1, u2 = 0, 0
        for die in range(3, 10):
            p1n = (p1 + die) % 10
            # u * PROBABILITIES[die] because we only consider the number of universes created by _this_ outcome
            # all of them together should add up to 27
            u1n, u2n = quantum(p1n, p2, s1 + p1n + 1, s2, u * PROBABILITIES[die], not turn)
            u1 += u1n
            u2 += u2n
        return (u1, u2)
    else:
        if s1 >= 21:
            return (u, 0)
        u1, u2 = 0, 0
        for die in range(3, 10):
            p2n = (p2 + die) % 10
            u1n, u2n = quantum(p1, p2n, s1, s2 + p2n + 1, u * PROBABILITIES[die], not turn)
            u1 += u1n
            u2 += u2n
        return (u1, u2)


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
