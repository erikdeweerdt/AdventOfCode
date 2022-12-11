from io import StringIO
import numpy as np

testdata = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''


class Operation:
    def __init__(self, expr) -> None:
        self.__expr = expr.replace('new = ', '')

    def apply(self, old):
        return eval(self.__expr)

    def __str__(self) -> str:
        return f'new = {self.__expr}'

    def __repr__(self) -> str:
        return str(self)


class Test:
    def __init__(self, test_string) -> None:
        self.__div = int(test_string.split(' ')[-1])

    def test(self, value):
        return value % self.__div == 0
    
    def get_div(self):
        return self.__div

    def __str__(self) -> str:
        return f'divisible by {self.__div}'

    def __repr__(self) -> str:
        return str(self)


class Monkey:
    def __init__(self, items, operation, test, if_true, if_false) -> None:
        self.__items = items
        self.__operation = operation
        self.__test = test
        self.__if_true = if_true
        self.__if_false = if_false
        self.__inspections = 0

    def turn(self, relief=True, lcm=None):
        if len(self.__items) == 0:
            raise StopIteration()
        self.__inspections += 1
        item = self.__operation.apply(self.__items.pop(0))
        # this keeps numbers manageable
        # divisibility doesn't change in modulo calculus
        # if we perform all calculations modulo the LCM of all monkey's divider, divisibility doesn't change for any of them
        if lcm is not None:
            item %= lcm
        if relief:
            item //= 3
        return (self.__if_true, item) if self.__test.test(item) else (self.__if_false, item)

    def add_item(self, item):
        self.__items.append(item)

    def activity(self):
        return self.__inspections

    def get_test(self):
        return self.__test

    def __str__(self) -> str:
        return f'Monkey({self.__inspections}) [{", ".join(str(item) for item in self.__items)}]\n  if({self.__operation} is {self.__test})\n    throw to {self.__if_true}\n  else\n    throw to {self.__if_false}'

    def __repr__(self) -> str:
        return str(self)


def part1():
    monkeys = list(read())
    for _ in range(20):
        for monkey in monkeys:
            while True:
                try:
                    (index, item) = monkey.turn()
                    monkeys[index].add_item(item)
                except StopIteration:
                    break
    monkeys.sort(key=lambda m: m.activity(), reverse=True)
    print(monkeys[0].activity() * monkeys[1].activity())


def part2():
    monkeys = list(read())
    lcm = np.lcm.reduce([m.get_test().get_div() for m in monkeys])
    for _ in range(10000):
        for monkey in monkeys:
            while True:
                try:
                    (index, item) = monkey.turn(False, lcm)
                    monkeys[index].add_item(item)
                except StopIteration:
                    break
    monkeys.sort(key=lambda m: m.activity(), reverse=True)
    print(monkeys[0].activity() * monkeys[1].activity())


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                if line.startswith('Starting items:'):
                    items = [int(i) for i in line[16:].split(', ')]
                elif line.startswith('Operation:'):
                    operation = Operation(line[11:])
                elif line.startswith('Test:'):
                    test = Test(line[5:])
                elif line.startswith('If true:'):
                    if_true = int(line[9:].split(' ')[-1])
                elif line.startswith('If false:'):
                    if_false = int(line[10:].split(' ')[-1])
                    yield Monkey(items, operation, test, if_true, if_false)


if __name__ == '__main__':
    # part1()
    part2()
