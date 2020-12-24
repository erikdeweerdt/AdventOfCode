import re
from typing import Dict, Iterable, List, Tuple

import numpy

# region testdata
TESTDATA = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""".splitlines()
# endregion


def parse_steps(data: List[str]) -> Iterable[List[str]]:
    for line in data:
        if line:
            yield re.findall(r"ne|nw|se|sw|e|w", line)


def step_to_delta(step: str) -> Tuple[float, float]:
    if step == "ne":
        return (.5, -1)
    if step == "nw":
        return (-.5, -1)
    if step == "se":
        return (.5, 1)
    if step == "sw":
        return (-.5, 1)
    if step == "e":
        return (1, 0)
    if step == "w":
        return (-1, 0)
    raise ValueError


def part1(data: List[str]):
    # tiles can be stored in a 2D list in wich every other row is shifted by 0.5
    # the grid is infinite, so we can't pre-generate such a list and have to use a sparse dict
    # we're counting black-side-up, so black = True
    tiles: Dict[Tuple(float, float), bool] = {(0, 0): False}
    for steps in parse_steps(data):
        coordinate = (0, 0)
        for step in steps:
            coordinate = tuple(numpy.add(coordinate, step_to_delta(step)))
        if coordinate in tiles:
            tiles[coordinate] = not tiles[coordinate]
        else:
            # tiles start out white, so the first flip makes them black
            tiles[coordinate] = True
    # print(tiles)
    print(sum(1 for tile in tiles.values() if tile))


if __name__ == "__main__":
    with open("data/24.txt") as f:
        data = f.read()
    data = data.splitlines()
    part1(data)
    # part1(["nwwswee"])
    # part2(data)
