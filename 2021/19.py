import re
import numpy as np
from itertools import combinations


def part1():
    beacons, _ = align_all(read())
    print(len(beacons))


def part2():
    _, positions = align_all(read())
    # manhattan distance = sum of straight-line distances in all directions
    print(max(np.abs(x-y).sum() for x, y in combinations(positions, 2)))


def align_all(scanners):
    distances = list(map(distance, scanners))
    # reference all scanner positions by the 0th one
    scanner_positions = {0: (0, 0, 0)}
    # deduplicated beacons: we'll add new ones after transforming them to the 0-reference
    beacons = set(map(tuple, scanners[0]))
    while len(scanner_positions) < len(scanners):
        for i, j, v in match(distances):
            # we're aligning against already known cubes: only consider those pairs for which one is already known
            if (i in scanner_positions) == (j in scanner_positions):
                continue
            # swap indexes if the second one is already known
            elif j in scanner_positions:
                i, j = j, i
            pos, b, r = align(scanners[i], scanners[j], distances[i][v], distances[j][v])
            # update the placement of the scanner in the grid
            # this allows newly added positions in the next iterations to be 0-referenced immediately
            scanner_positions[j] = pos
            scanners[j] = r(scanners[j]) + pos
            beacons.update(b)
    return beacons, scanner_positions.values()


def align(s1, s2, p1, p2):
    for r in rotations():
        s2t = r(s2)
        # p1 and p2 are point pairs that can align either way
        p = p1[0]
        for q in p2:
            d = s1[p, :] - s2t[q, :]
            if len((b := set(map(tuple, s2t + d))) & set(map(tuple, s1))) >= 12:
                # return
                # * the distance (i.e. how much the j scanner is translated w.r.t to the i one)
                # * the overlapping beacons
                # * the rotation used
                return d, b, r


def match(distances):
    for i, j in combinations(range(len(distances)), 2):
        # 66 = number of combinations of 2 elements out of 12, i.e. all possible distances between pairs (excluding reverse direction)
        # = (12 * 11) / 2
        if len(m := set(distances[i]) & set(distances[j])) >= 66:
            # return the matching indexes (i.e. scanners) and some matching distance pair (e.g. the first one)
            yield i, j, next(iter(m))


def distance(scanner):
    # calculate absolute distances between beacons among every axis
    # sort by magnitude (sum could also be used, but that may leave a bigger search space)
    # use as key in map to facilitate set operations
    return {
        tuple(sorted(map(abs, scanner[i, :] - scanner[j, :]))): (i, j)
        for i, j in combinations(range(len(scanner)), 2)
    }


def rotations():
    # possible orientations
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
                yield lambda x: np.matmul(x, np.array([vi, vj, vk]))


def read():
    scanners = []
    with open("data/19.txt") as f:
        # data =f.read()
        for l in f.readlines():
            if l.strip():
                if re.match(r'--- scanner \d+ ---', l):
                    s = []
                    scanners.append(s)
                else:
                    s.append(list(map(int, l.split(','))))
    scanners = list(map(np.array, scanners))
    return scanners


if __name__ == '__main__':
    part1()
    part2()
