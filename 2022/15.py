import re
from bisect import bisect_left
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

    def no_beacons(self, y):
        max_distance = manhattan(self.__pos, self.__closest_beacon)
        y_distance = manhattan(self.__pos, (self.__pos[0], y))
        d = max_distance - y_distance
        if d < 0:
            return None
        # ignore the presence of any beacons
        return (self.__pos[0] - d, self.__pos[0] + d)

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
        ranges = []
        for sensor in self.__sensors:
            if r := sensor.no_beacons(row):
                ranges = insert_range(ranges, r)
        # print(empty)
        # print(''.join('#' if (i,row) in empty else '.' for i in range(-5,27)))
        beacons_in_range = sum(range_contains_count(r, (b[0] for b in self.__beacons if b[1] == row)) for r in ranges)
        return sum(r[1] - r[0] + 1 for r in ranges) - beacons_in_range

    def __str__(self) -> str:
        return '\n'.join(str(sensor) for sensor in self.__sensors)

    def __repr__(self) -> str:
        return str(self)


def manhattan(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])


def insert_range(ranges, ran):
    # bisect in Python 3.8 can't use a key (for a bogus reason, which is why they added it in 3.10)
    index = bisect_left([r[0] for r in ranges], ran[0])
    # print(ranges,ran)
    new_ranges = ranges[:index]
    if index > 0 and ran[0] <= new_ranges[index-1][1]:
        if ran[1] > new_ranges[index-1][1]:
            ran = (new_ranges[index-1][0], ran[1])
            new_ranges[index-1] = ran
    else:
        new_ranges.append(ran)
    for r in ranges[index:]:
        if ran[1] >= r[1]:
            continue
        elif ran[1] >= r[0]:
            new_ranges[-1] = (ran[0], r[1])
        else:
            new_ranges.append(r)
    # print(new_ranges)
    # print()
    return new_ranges

def range_contains_count(range, points):
    count = 0
    for p in points:
        if p >= range[0] and p <= range[1]:
            count += 1
    return count


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
    part1()  # 5112034
    # part2()
