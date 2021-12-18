import json
import math
from functools import reduce

LEFT = 0
RIGHT = 1

TESTDATA = [
    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
    '[7,[5,[[3,8],[1,4]]]]',
    '[[2,[2,2]],[8,[8,1]]]',
    '[2,9]',
    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
    '[[[5,[7,4]],7],1]',
    '[[[[4,2],2],6],[8,7]]',
]


class Node:
    def __init__(self, pair=None, parent=None):
        self.__parent = parent
        if type(pair) is str:
            pair = json.loads(pair)
        if type(pair) is list:
            self.__value = None
            self.__left = Node(pair[0], self)
            self.__right = Node(pair[1], self)
        else:
            self.__value = pair
            self.__left = None
            self.__right = None

    def __str__(self):
        if self.__value is not None:
            return str(self.__value)
        return f'[{self.__left}, {self.__right}]'

    def __add__(self, other):
        node = Node()
        self.__parent = node
        other.__parent = node
        node.__left = self
        node.__right = other
        return node.reduce()

    def magnitude(self):
        if self.__value is not None:
            return self.__value
        return 3 * self.__left.magnitude() + 2 * self.__right.magnitude()

    def reduce(self):
        while True:
            if self.explode():
                # print('E', self)
                continue
            if self.split():
                # print('S', self)
                continue
            break
        return self

    def explode(self, level=0):
        if self.__value is None:
            if level >= 4:
                if s := self.__sibling(LEFT):
                    s.__add(self.__left.__value, RIGHT)
                if s := self.__sibling(RIGHT):
                    s.__add(self.__right.__value, LEFT)
                self.__value = 0
                self.__left = None
                self.__right = None
                return True
            else:
                if self.__left.explode(level + 1):
                    return True
                if self.__right.explode(level + 1):
                    return True
        return False

    def split(self):
        if self.__value is not None:
            if self.__value >= 10:
                v = self.__value / 2
                self.__value = None
                self.__left = Node(math.floor(v))
                self.__right = Node(math.ceil(v))
                self.__left.__parent = self
                self.__right.__parent = self
                return True
        else:
            if self.__left.split():
                return True
            if self.__right.split():
                return True
        return False

    def __sibling(self, lr):
        s = self
        p = self.__parent
        while p and (p.__left, p.__right)[lr] == s:
            s = p
            p = s.__parent
        if p:
            return (p.__left, p.__right)[lr]
        return None

    def __add(self, value, lr):
        s = self
        while s.__value is None:
            s = (s.__left, s.__right)[lr]
        s.__value += value


def part1():
    fishes = read()
    f = reduce(lambda a, b: a + Node(b), fishes, Node(fishes[0]))
    print(f, f.magnitude())


def part2():
    fishes = read()
    mag = 0
    for a in fishes:
        for b in fishes:
            if a is not b:
                # addition modifies the original node (yeah, dirty, I know)
                # so re-create nodes every time
                mag = max(mag, (Node(a) + Node(b)).magnitude())
    print(mag)


def read():
    with open("data/18.txt") as f:
        data = [l.strip() for l in f.readlines() if l.strip()]
    return data
    # return [l for l in TESTDATA]


if __name__ == '__main__':
    part1()
    part2()
