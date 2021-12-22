import re
from itertools import product


class Step:
    def __init__(self, step):
        if m := re.match(r'^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', step):
            self.on = m.group(1) == 'on'
            self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = map(int, m.groups()[1:])
        else:
            raise ValueError()

    def __str__(self):
        return f'{"on" if self.on else "off"} x={self.xmin}..{self.xmax},y={self.ymin}..{self.ymax},z={self.zmin}..{self.zmax}'


def part1():
    steps = read()
    # naive approach for part 1: just store all cubes that are on
    reactor = set()
    for step in steps:
        if max(abs(step.xmin), abs(step.xmax), abs(step.ymin), abs(step.ymax), abs(step.zmin), abs(step.zmax)) > 50:
            # we'll see if anything overlaps...
            break
        for p in product(range(step.xmin, step.xmax + 1), range(step.ymin, step.ymax + 1), range(step.zmin, step.zmax + 1)):
            if step.on:
                reactor.add(p)
            else:
                try:
                    reactor.remove(p)
                except KeyError:
                    pass
    print(len(reactor))


def part2():
    pass


def read():
    with open("data/22.txt") as f:
        steps = map(Step, f.readlines())
    return list(steps)


if __name__ == '__main__':
    part1()
    part2()
