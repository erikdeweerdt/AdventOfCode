import statistics

TESTDATA = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '{([(<{}[<>[]}>{[]{[(<()>',
    '(((({<>}<{<{<>}{[]{[]{}',
    '[[<[([]))<([[{}[[()]]]',
    '[{[{({}]{}}([{[{{{}}([]',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '[<(<(<(<{}))><([]([]()',
    '<{([([[(<>()){}]>(<<{{',
    '<{([{{}}[<[[[<>{}]]]>[]]',
]

PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
SSCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
ASCORES = {')': 1, ']': 2, '}': 3, '>': 4}


def part1():
    with open("data/10.txt") as f:
        data = [l.strip() for l in f.readlines() if l]
    errors = (check(l) for l in data)
    # print(list(errors))
    print(sum(SSCORES[e] for e in errors if type(e) is str))


def part2():
    with open("data/10.txt") as f:
        data = [l.strip() for l in f.readlines() if l]
    errors = (check(l) for l in data)
    # the winner is the middle score
    print(statistics.median(e for e in errors if type(e) is int))


def check(line):
    stack = []
    for c in line:
        if c in PAIRS.keys():
            stack.append(c)
        elif len(stack) == 0:
            return c
        elif c != PAIRS[stack.pop()]:
            return c
    return complete(stack)


def complete(stack):
    score = 0
    for c in reversed(stack):
        score *= 5
        score += ASCORES[PAIRS[c]]
    return score


if __name__ == '__main__':
    # part1()
    part2()
