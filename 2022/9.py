from io import StringIO

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

movements = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}


class Rope:
    def __init__(self) -> None:
        self.__head = (0, 0)
        self.__tail = (0, 0)
        self.__bounds = ((0, 0), (0, 0))
        self.__visited = set()

    def move_head(self, direction):
        mx, my = movements[direction]
        self.__head = (self.__head[0]+mx, self.__head[1]+my)
        self.__move_tail()
        self.__update_bounds()

    def visited_count(self):
        return len(self.__visited)

    def __move_tail(self):
        dx, dy = (self.__head[0] - self.__tail[0], self.__head[1] - self.__tail[1])
        if abs(dx) == 2:
            self.__tail = (self.__tail[0] + dx // 2, self.__tail[1] + dy)
        elif abs(dy) == 2:
            self.__tail = (self.__tail[0] + dx, self.__tail[1] + dy // 2)
        self.__visited.add(self.__tail)

    def __update_bounds(self):
        self.__bounds = ((min(self.__bounds[0][0], self.__head[0], self.__tail[0]), min(self.__bounds[0][1], self.__head[1], self.__tail[1])),
                         (max(self.__bounds[1][0], self.__head[0], self.__tail[0]), max(self.__bounds[1][1], self.__head[1], self.__tail[1])))

    def __str__(self):
        res = []
        for y in range(self.__bounds[0][1], self.__bounds[1][1] + 1):
            row = []
            for x in range(self.__bounds[0][0], self.__bounds[1][0] + 1):
                if (x,y) == self.__head:
                    char = 'H'
                elif (x,y) == self.__tail:
                    char = 'T'
                elif (x,y) in self.__visited:
                    char = '#'
                else:
                    char = '.'
                row.append(char)
            res.append(''.join(row))
        return '\n'.join(reversed(res))

    def __repr__(self):
        return str(self)


def part1():
    rope = Rope()
    for move in read():
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
    part1()
    # part2()
