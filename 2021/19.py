import re
import numpy as np
from itertools import combinations, product


class Rotation:
    __all = None

    def __init__(self, matrix):
        self.__matrix = matrix

    def apply(self, vector):
        return np.matmul(vector, self.__matrix)

    @classmethod
    def all(cls):
        if cls.__all is None:
            cls.__all = []
            # rotations are defined by picking x and y,
            # filtering out those combinations that are parallel (dot product == 0)
            # and then finding z with the cross product
            # see https://stackoverflow.com/questions/34391968/how-to-find-the-rotation-matrix-between-two-coordinate-systems
            # the translation component can be ignored because coordinates are relative
            vectors = [
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            ]
            vectors = list(map(np.array, vectors))
            # pick x and y orientation
            for vi in vectors:
                for vj in vectors:
                    # if dot product is 0 both are parallel and thus invalid
                    if vi.dot(vj) == 0:
                        # otherwise z is the cross product
                        vk = np.cross(vi, vj)
                        cls.__all.append(cls(np.array([vi, vj, vk])))
        return cls.__all


class Scanner:
    def __init__(self, id) -> None:
        self.pos = np.array([0, 0, 0]) if id == 0 else None
        self.__beacons = None
        self.__distances = {}

    def add_beacon(self, beacon):
        b = np.array(list(map(int, beacon.split(','))))
        if self.__beacons is None:
            self.__beacons = b
        else:
            j = len(self.__beacons) if len(self.__beacons.shape) == 2 else 1
            self.__beacons = np.vstack((self.__beacons, b))
            # calculate and store distances from the new beacon to the existing ones
            for i in range(j):
                self.__distances[self.__distance(self.__beacons[i, :], b)] = (i, j)

    @property
    def beacons(self):
        yield from map(tuple, self.__beacons)

    def match(self, other):
        # 66 = number of combinations of 2 elements out of 12, i.e. all possible distances between pairs (excluding reverse direction)
        # = (12 * 11) / 2
        # if there's a match, return some matching distance
        if len(m := set(self.__distances) & set(other.__distances)) >= 66:
            # a set is not indexed
            return next(iter(m))
        return None

    def align(self, other, matching_distance):
        # attempt to align other to self, starting with the point pairs with matching distance
        # take the first point of self and attempt for both of the second (pairs can align either way)
        # if successful, transform other into self's coordinate system
        sb = self.__beacons
        for r in Rotation.all():
            ob = r.apply(other.__beacons)
            p = self.__distances[matching_distance][0]
            for q in other.__distances[matching_distance]:
                # translate point q to p and check if at least 12 points in total now line up
                d = sb[p, :] - ob[q, :]
                if len((b := set(map(tuple, ob + d))) & set(map(tuple, sb))) >= 12:
                    # transform other
                    if other.pos:
                        other.pos += d
                    else:
                        other.pos = d
                    other.__beacons = ob + d
                    # return the set of matching beacons
                    return b
        return None

    @staticmethod
    def __distance(a, b):
        # sort distances since we don't know which component is which after rotation
        # we could also take the sum, but that increases the chance of collisions
        return tuple(sorted(map(abs, a - b)))


def part1():
    scanners = read()
    beacons = align_all(scanners)
    print(len(beacons))


def part2():
    scanners = read()
    align_all(scanners)
    print(max(np.abs(x.pos-y.pos).sum() for x, y in combinations(scanners, 2)))


def align_all(scanners):
    found = scanners[0:1]
    todo = scanners[1:]
    beacons = set(scanners[0].beacons)
    while todo:
        for a, b in product(found, todo):
            if m := a.match(b):
                beacons.update(a.align(b, m))
                found.append(b)
                todo.remove(b)
                break
    return beacons


def read():
    scanners = []
    with open("data/19.txt") as f:
        for l in f.readlines():
            if l.strip():
                if m := re.match(r'--- scanner (\d+) ---', l):
                    s = Scanner(int(m.group(1)))
                    scanners.append(s)
                else:
                    s.add_beacon(l.strip())
    return scanners


if __name__ == '__main__':
    part1()  # 436
    part2()  # 10918
