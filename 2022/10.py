from abc import ABC
from io import StringIO

testdata = '''
noop
addx 3
addx -5
'''

testdata2 = '''
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''


class Instruction(ABC):
    def __init__(self, duration, value) -> None:
        self.__duration = duration
        self._value = value

    def cycle(self):
        self.__duration -= 1
        if self.__duration <= 0:
            return self._value
        return None


class AddX(Instruction):
    def __init__(self, value) -> None:
        super().__init__(2, value)

    def __str__(self):
        return f'addx {self._value}'

    def __repr__(self):
        return str(self)


class Noop(Instruction):
    def __init__(self) -> None:
        super().__init__(1, 0)

    def __str__(self):
        return 'noop'

    def __repr__(self):
        return str(self)


class CPU:
    def __init__(self) -> None:
        self.__x = 1
        self.__cycle = 0
        self.__instructions = []

    def cycle(self):
        self.__cycle += 1
        if len(self.__instructions) == 0:
            return
        v = self.__instructions[0].cycle()
        if v is not None:
            self.__x += v
            self.__instructions.pop(0)

    def add_instruction(self, instruction):
        self.__instructions.append(instruction)

    def signal_strength(self):
        # signal strength is defined as _during_ the cycle, i.e. before handling instructions and increasing the counter
        return (self.__cycle + 1) * self.__x

    def __str__(self) -> str:
        return f'{self.__cycle:03} ({self.__x}) [{", ".join(str(instr) for instr in self.__instructions)}]'


def part1():
    # note: the requested result is the value _during_ the cycle, so before calling cpu.cycle()
    cpu = CPU()
    data = iter(read())
    signal_strengths = []
    for i in range(220):
        try:
            cpu.add_instruction(next(data))
        except StopIteration:
            pass
        if i + 1 in [20,60,100,140,180,220]:
            signal_strengths.append(cpu.signal_strength())
        cpu.cycle()
        # print(cpu)
    print(signal_strengths)
    print(sum(signal_strengths))


def part2():
    pass


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                if line.startswith('noop'):
                    yield Noop()
                else:
                    yield AddX(int(line[5:]))


if __name__ == '__main__':
    part1()
    # part2()
