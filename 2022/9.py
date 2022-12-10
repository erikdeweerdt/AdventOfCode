from io import StringIO
from math import copysign

testdata = '''
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

testdata2 = '''
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

movements = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}


class Rope:
    def __init__(self, length) -> None:
        self.__length = length
        self.__knots = [(0, 0) for _ in range(length)]
        self.__bounds = ((0, 0), (0, 0))
        self.__visited = set()

    def move_head(self, direction):
        head = self.__knots[0]
        mx, my = movements[direction]
        head = (head[0]+mx, head[1]+my)
        self.__knots[0] = head
        for i in range(1, self.__length):
            self.__move_knot(i)
        self.__update_bounds()

    def visited_count(self):
        return len(self.__visited)

    def __move_knot(self, index):
        prev = self.__knots[index - 1]
        knot = self.__knots[index]
        dx, dy = (prev[0] - knot[0], prev[1] - knot[1])
        if abs(dx) == 2:
            knot = (knot[0] + dx // 2, knot[1] + int(copysign(1 if dy != 0 else 0, dy)))
        elif abs(dy) == 2:
            knot = (knot[0] + int(copysign(1 if dx != 0 else 0, dx)), knot[1] + dy // 2)
        elif abs(dx) > 2 or abs(dy) > 2:
            raise Exception('Jerk')
        self.__knots[index] = knot
        if index == self.__length - 1:
            self.__visited.add(knot)

    def __update_bounds(self):
        self.__bounds = ((min(self.__bounds[0][0], min(k[0] for k in self.__knots)), min(self.__bounds[0][1], min(k[1] for k in self.__knots))),
                         (max(self.__bounds[1][0], max(k[0] for k in self.__knots)), max(self.__bounds[1][1], max(k[1] for k in self.__knots))))

    def __str__(self):
        res = []
        for y in range(self.__bounds[0][1], self.__bounds[1][1] + 1):
            row = []
            for x in range(self.__bounds[0][0], self.__bounds[1][0] + 1):
                char = '.'
                # for i, knot in enumerate(self.__knots):
                #     if (x, y) == knot:
                #         char = str(i)
                #         break
                if (x, y) in self.__visited:
                    char = '#'
                row.append(char)
            res.append(''.join(row))
        return '\n'.join(reversed(res))

    def __repr__(self):
        return str(self)


def part1():
    rope = Rope(2)
    for move in read():
        # print(move)
        rope.move_head(move)
        # print(rope)
        # print()
    # print(rope)
    print(rope.visited_count())


def part2():
    rope = Rope(10)
    for move in read():
        # print(rope)
        # print(move)
        rope.move_head(move)
        # print(rope)
        # print()
    # print(rope)
    print(rope.visited_count())


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                direction, count = line.split(' ', 1)
                for _ in range(int(count)):
                    yield direction


if __name__ == '__main__':
    # part1()
    part2()
