from io import StringIO

testdata = '''
30373
25512
65332
33549
35390
'''


class Tree():
    def __init__(self, height) -> None:
        self.height = int(height)
        self.highest = None

    def __str__(self):
        # return str(self.height)
        # return f'{self.height}[{"V" if self.height > self.highest else " "}]'
        return f'{self.height}[{self.highest}]'

    def __repr__(self):
        return str(self)


def scan(trees):
    highest = -1
    for tree in trees:
        if tree.highest is None or tree.highest > highest:
            tree.highest = highest
        if tree.height == 9:
            break
        highest = max(highest, tree.height)


def viewing_distance(forest, rows, cols, r, c):
    if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
        return 0
    tree = forest[r][c]
    up = 0
    down = 0
    left = 0
    right = 0
    for up in range(1, r + 1):
        if forest[r-up][c].height >= tree.height:
            break
    for down in range(1, rows - r):
        if forest[r+down][c].height >= tree.height:
            break
    for left in range(1, c + 1):
        if forest[r][c-left].height >= tree.height:
            break
    for right in range(1, cols - c):
        if forest[r][c+right].height >= tree.height:
            break
    return up * down * left * right


def part1():
    forest = read()
    rows = len(forest)
    cols = len(forest[0])
    for r in range(rows):
        scan(forest[r][c] for c in range(cols))
        scan(forest[r][c] for c in reversed(range(cols)))
    for c in range(cols):
        scan(forest[r][c] for r in range(rows))
        scan(forest[r][c] for r in reversed(range(rows)))
    count = sum(0 if tree.highest is None or tree.height <= tree.highest else 1 for row in forest for tree in row)
    # print(forest)
    print(count)


def part2():
    forest = read()
    rows = len(forest)
    cols = len(forest[0])
    v = max(viewing_distance(forest, rows, cols, r, c) for r in range(rows) for c in range(cols))
    # v = viewing_distance(forest, rows, cols, 3, 2)
    print(v)


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        data = list(map(str.strip, f.readlines()))
    forest = []
    for line in data:
        if line:
            forest.append(list(map(Tree, line)))
    return forest


if __name__ == '__main__':
    part1()
    part2()
