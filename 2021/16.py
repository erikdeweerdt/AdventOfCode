from abc import ABC, abstractmethod
from functools import reduce


class Bitstream:
    def __init__(self, data):
        self.__data = data
        self.__ptr = 0
        self.__bfr = None

    def read_bit(self):
        ptr = self.__ptr % 4
        if ptr == 0:
            pos = self.__ptr // 4
            if pos >= len(self.__data):
                return None
            self.__bfr = int(self.__data[pos], 16)
        bit = self.__bfr >> (3 - ptr) & 1
        self.__ptr += 1
        return bit

    def read_bits(self, n):
        bits = 0
        for _ in range(n):
            bits = bits * 2 + self.read_bit()
        return bits


class Packet(ABC):
    def __init__(self, version, type):
        self.version = version
        self.type = type

    @abstractmethod
    def length(self):
        return 6

    @abstractmethod
    def evaluate(self):
        return None

    @staticmethod
    def create_packet(stream):
        v = stream.read_bits(3)
        t = stream.read_bits(3)
        if t == 4:
            p = Literal(v, t)
        else:
            p = Operator(v, t)
        p.read(stream)
        return p


class Literal(Packet):
    def __init__(self, version, type):
        # type must be 4, but don't care to check that
        super().__init__(version, type)
        self.__value = 0
        self.__length = 6

    def __str__(self):
        return str(self.__value)

    def __iter__(self):
        yield self

    def read(self, stream):
        while True:
            self.__length += 5
            bits = stream.read_bits(5)
            # print(f'{bits:b}')
            self.__value = self.__value * 16 + (bits & 15)
            if bits & 16 == 0:
                break

    def length(self):
        return self.__length

    def evaluate(self):
        return self.__value


class Operator(Packet):
    __evaluators = {
        0: ('sum', lambda p: reduce(lambda a, b: a + b.evaluate(), p, 0)),
        1: ('prod', lambda p: reduce(lambda a, b: a * b.evaluate(), p, 1)),
        2: ('min', lambda p: reduce(lambda a, b: min(a, b.evaluate()), p, float('inf'))),
        3: ('max', lambda p: reduce(lambda a, b: max(a, b.evaluate()), p, float('-inf'))),
        5: ('gt', lambda p: 1 if p[0].evaluate() > p[1].evaluate() else 0),
        6: ('lt', lambda p: 1 if p[0].evaluate() < p[1].evaluate() else 0),
        7: ('eq', lambda p: 1 if p[0].evaluate() == p[1].evaluate() else 0),
    }

    def __init__(self, version, type):
        super().__init__(version, type)
        self.__length_type = None
        self.__length = None
        self.__packets = []

    def __str__(self):
        return self.__evaluators[self.type][0] + '(' + ', '.join(str(p) for p in self.__packets) + ')'

    def __iter__(self):
        yield self
        for p in self.__packets:
            yield from p

    def read(self, stream):
        self.__length_type = stream.read_bit()
        self.__length = stream.read_bits(15 if self.__length_type == 0 else 11)
        remainder = self.__length
        while remainder > 0:
            self.__packets.append(p := Packet.create_packet(stream))
            remainder -= 1 if self.__length_type == 1 else p.length()

    def length(self):
        if self.__length_type == 0:
            return 22 + self.__length
        if self.__length_type == 1:
            return 18 + sum(p.length() for p in self.__packets)
        return None

    def evaluate(self):
        return self.__evaluators[self.type][1](self.__packets)


def part1():
    bs = Bitstream(read())
    packet = Packet.create_packet(bs)
    print(packet)
    print(sum(p.version for p in packet))


def part2():
    bs = Bitstream(read())
    packet = Packet.create_packet(bs)
    print(packet)
    print(packet.evaluate())


def read():
    with open("data/16.txt") as f:
        data = f.readline().strip()
    return data


if __name__ == '__main__':
    # part1()
    part2()
