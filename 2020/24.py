import re
import sys
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


def make_grid(data: List[str]) -> Dict[Tuple[float, float], bool]:
    # tiles can be stored in a 2D list in wich every other row is shifted by 0.5
    # the grid is infinite, so we can't pre-generate such a list and have to use a sparse dict
    # we're counting black-side-up, so black = True
    tiles = {(0, 0): False}
    for steps in parse_steps(data):
        coordinate = (0, 0)
        for step in steps:
            coordinate = tuple(numpy.add(coordinate, step_to_delta(step)))
        if coordinate in tiles:
            tiles[coordinate] = not tiles[coordinate]
        else:
            # tiles start out white, so the first flip makes them black
            tiles[coordinate] = True
    return tiles


def ensure_neigbors(grid: Dict[Tuple[float, float], bool], coordinate: Tuple[float, float]):
    for delta in [(.5, -1), (-.5, -1), (.5, 1), (-.5, 1), (1, 0), (-1, 0)]:
        c = tuple(numpy.add(coordinate, delta))
        if c not in grid:
            grid[c] = False


def neighbors(grid: Dict[Tuple[float, float], bool], coordinate: Tuple[float, float]) -> Iterable[bool]:
    for delta in [(.5, -1), (-.5, -1), (.5, 1), (-.5, 1), (1, 0), (-1, 0)]:
        c = tuple(numpy.add(coordinate, delta))
        if c in grid:
            yield grid[c]


def flip_tiles(grid: Dict[Tuple[float, float], bool]):
    flip = []
    for coordinate, tile in grid.items():
        black_neighbors = sum(1 for neighbor in neighbors(
            grid, coordinate) if neighbor)
        if tile and (black_neighbors == 0 or black_neighbors > 2):
            flip.append(coordinate)
        elif not tile and black_neighbors == 2:
            flip.append(coordinate)
    for coordinate in flip:
        grid[coordinate] = not grid[coordinate]
        if grid[coordinate]:
            ensure_neigbors(grid, coordinate)


def part1(data: List[str]):
    grid = make_grid(data)
    # print(grid)
    print(sum(1 for tile in grid.values() if tile))


def part2(data: List[str]):
    grid = make_grid(data)
    # make sure all black tiles have all neighbors
    for coordinate in [coordinate for coordinate in grid if grid[coordinate]]:
        ensure_neigbors(grid, coordinate)
    for _ in range(100):
        flip_tiles(grid)
        print(".", end="")
        sys.stdout.flush()
    print()
    print(sum(1 for tile in grid.values() if tile))


if __name__ == "__main__":
    with open("data/24.txt") as f:
        data = f.read()
    data = data.splitlines()
    # part1(data)
    part2(data)
