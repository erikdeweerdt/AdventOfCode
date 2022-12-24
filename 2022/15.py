import re
from io import StringIO

testdata = '''
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''


class Sensor:
    def __init__(self, pos, closest_beacon) -> None:
        self.__pos = pos
        self.__closest_beacon = closest_beacon

    def no_beacons(self, y, all_beacons):
        max_distance = manhattan(self.__pos, self.__closest_beacon)
        for x in range(self.__pos[0] - max_distance, self.__pos[0] + max_distance + 1):
            if manhattan((x, y), self.__pos) <= max_distance and (x, y) not in all_beacons:
                yield (x, y)

    def __eq__(self, obj):
        return isinstance(obj, Sensor) and obj.__pos == self.__pos

    def __ne__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self) -> int:
        return hash(self.__pos)

    def __str__(self):
        return f'Sensor at x={self.__pos[0]}, y={self.__pos[1]}: closest beacon is at x={self.__closest_beacon[0]}, y={self.__closest_beacon[1]}'

    def __repr__(self) -> str:
        return str(self)


class Cave:
    def __init__(self) -> None:
        self.__sensors = set()
        self.__beacons = set()

    def add_data(self, data):
        pattern = re.compile(
            r'^Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)$')
        if match := pattern.match(data):
            beacon = (int(match.group('bx')), int(match.group('by')))
            sensor = Sensor((int(match.group('sx')), int(match.group('sy'))), beacon)
            self.__beacons.add(beacon)
            self.__sensors.add(sensor)
        else:
            raise ValueError(f'Invalid data: {data}')

    def count_row(self, row):
        empty = set()
        for sensor in self.__sensors:
            for b in sensor.no_beacons(row, self.__beacons):
                empty.add(b)
        # print(empty)
        # print(''.join('#' if (i,row) in empty else '.' for i in range(-5,27)))
        return len(empty)

    def __str__(self) -> str:
        return '\n'.join(str(sensor) for sensor in self.__sensors)

    def __repr__(self) -> str:
        return str(self)


def manhattan(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def part1():
    cave = Cave()
    for line in read():
        cave.add_data(line)
    print(cave)
    print()
    print(cave.count_row(2000000))


def part2():
    pass


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        while line := f.readline():
            if line := line.strip():
                yield line


if __name__ == '__main__':
    part1() # 5112034
    # part2()
