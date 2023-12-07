from io import StringIO
from os import path

testdata = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''


def part1():
    hands = []
    for line in read():
        hand, bid = line.split(' ')
        hands.append((hand, int(bid)))
    hands.sort(key=lambda h: score_hand(h[0], False))
    # print(hands)
    winnings = sum(h[1] * (i + 1) for i, h in enumerate(hands))
    print(winnings)


def part2():
    hands = []
    for line in read():
        hand, bid = line.split(' ')
        # print(hand, label_hand(hand, True))
        hands.append((hand, int(bid)))
    hands.sort(key=lambda h: score_hand(h[0], True))
    # print(hands)
    winnings = sum(h[1] * (i + 1) for i, h in enumerate(hands))
    print(winnings)


def score_hand(hand, joker):
    # [::-1] reverses the string
    cards = ('AKQT98765432J' if joker else 'AKQJT98765432')[::-1]
    _, s = label_hand(hand, joker)
    for token in hand:
        s *= 13
        s += cards.index(token)
    return s


def label_hand(hand, joker):
    tokens = {}
    jokers = 0
    for token in hand:
        if joker and token == 'J':
            jokers += 1
        else:
            tokens[token] = tokens.get(token, 0) + 1
    tokens = list(tokens.values())
    tokens.sort()
    if joker and jokers > 0:
        # if there are 4, all match the single non-joker
        if len(tokens) <= 1:
            return 'five of a kind', 7
        if jokers == 3:
            return 'four of a kind', 6
        if jokers == 2:
            # if you can make a full house using jokers, you can always make four of a kind as well (which is better)
            if len(tokens) == 2:
                return 'four of a kind', 6
            return 'three of a kind', 4
        # if there's only 1 joker, just fall back to normal flow (add it to the biggest pile)
        tokens[-1] += 1
    if len(tokens) == 5:
        return 'high card', 1
    if len(tokens) == 4:
        return 'one pair', 2
    if len(tokens) == 3:
        if tokens[-1] == 3:
            return 'three of a kind', 4
        return 'two pair', 3
    if len(tokens) == 2:
        if tokens[-1] == 4:
            return 'four of a kind', 6
        return 'full house', 5
    return 'five of a kind', 7


def read(data=None):
    with StringIO(data) if data else open(f'data/{path.basename(__file__).replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    # part1()
    part2()
