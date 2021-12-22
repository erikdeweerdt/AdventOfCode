import re
from itertools import chain, combinations, product


class Cuboid:
    def __init__(self, step=None, cuboid=None, on=None, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):
        if step:
            if m := re.match(r'^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', step):
                self.on = m.group(1) == 'on'
                self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = map(int, m.groups()[1:])
            else:
                raise ValueError()
        elif cuboid:
            self.on, self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = cuboid.on, cuboid.xmin, cuboid.xmax, cuboid.ymin, cuboid.ymax, cuboid.zmin, cuboid.zmax
        else:
            self.on, self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax = on, xmin, xmax, ymin, ymax, zmin, zmax

    def __str__(self):
        return f'{"on" if self.on else "off"} x={self.xmin}..{self.xmax},y={self.ymin}..{self.ymax},z={self.zmin}..{self.zmax}'

    def volume(self):
        return (self.xmax - self.xmin + 1) * (self.ymax - self.ymin + 1) * (self.zmax - self.zmin + 1)

    def intersects(self, other):
        if self.xmin > other.xmax or other.xmin > self.xmax:
            return False
        if self.ymin > other.ymax or other.ymin > self.ymax:
            return False
        if self.zmin > other.zmax or other.zmin > self.zmax:
            return False
        return True

    def intersection(self, other):
        # return the intersection cuboid (intersects must be true)
        # the intersection has the state of the overlayed cuboid
        return Cuboid(
            on=other.on,
            xmin=max(self.xmin, other.xmin),
            xmax=min(self.xmax, other.xmax),
            ymin=max(self.ymin, other.ymin),
            ymax=min(self.ymax, other.ymax),
            zmin=max(self.zmin, other.zmin),
            zmax=min(self.zmax, other.zmax)
        )

    def minus(self, other):
        # return a set of cuboids that comprise this one, except other
        # other must exist entirely within self, as produced by intersection
        # this also needs to be done if the cuboid being removed has the same state to prevent counting it multiple times
        if other.xmin > self.xmin:
            c = Cuboid(cuboid=self)
            c.xmax = other.xmin - 1
            yield c
        if other.xmax < self.xmax:
            c = Cuboid(cuboid=self)
            c.xmin = other.xmax + 1
            yield c
        if other.ymin > self.ymin:
            c = Cuboid(cuboid=self)
            c.xmin = other.xmin
            c.xmax = other.xmax
            c.ymax = other.ymin - 1
            yield c
        if other.ymax < self.ymax:
            c = Cuboid(cuboid=self)
            c.xmin = other.xmin
            c.xmax = other.xmax
            c.ymin = other.ymax + 1
            yield c
        if other.zmin > self.zmin:
            c = Cuboid(cuboid=self)
            c.xmin = other.xmin
            c.xmax = other.xmax
            c.ymin = other.ymin
            c.ymax = other.ymax
            c.zmax = other.zmin - 1
            yield c
        if other.zmax < self.zmax:
            c = Cuboid(cuboid=self)
            c.xmin = other.xmin
            c.xmax = other.xmax
            c.ymin = other.ymin
            c.ymax = other.ymax
            c.zmin = other.zmax + 1
            yield c


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
    steps = read()
    volume = 0
    # this loop keeps dividing up cuboids until none of them intersect with each other
    while steps:
        s = steps.pop(0)
        try:
            # find first intersect
            i = next(i for i, t in enumerate(steps) if s.intersects(t))
            t = steps[i]
            intersect = s.intersection(t)
            ms = list(s.minus(intersect))
            mt = list(t.minus(intersect))
            # ordering is important: on + on + off != on + off + on
            # insert the new cuboids where the old ones were removed
            # the relative order of the new cuboids is not important as they don't intersect
            steps = [intersect] + ms + steps[:i] + mt + steps[i+1:]
        except StopIteration:
            # no intersects -> done with this
            # only "on" cuboids are being counted, so discard the other ones
            if s.on:
                volume += s.volume()
    print(volume)


def read():
    with open("data/22.txt") as f:
        steps = map(Cuboid, f.readlines())
    return list(steps)


if __name__ == '__main__':
    # part1()
    part2()
