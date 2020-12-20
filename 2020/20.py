import math
import re
from typing import Dict, Iterable, List, Optional, Tuple

# region testdata
TESTDATA = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""".splitlines()
# endregion


class Border:
    def __init__(self, pixels: List[List[bool]] = None, n: int = 0, e: int = 0, s: int = 0, w: int = 0):
        if pixels:
            # pixels are ordered such that corresponding borders can directly be compared
            # this makes rotation more costly, but we're doing that only once
            self.n = sum(2**pos if pixels[0][pos] else 0 for pos in range(10))
            self.e = sum(2**pos if pixels[pos][-1] else 0 for pos in range(10))
            self.s = sum(2**pos if pixels[-1][pos]else 0 for pos in range(10))
            self.w = sum(2**pos if pixels[pos][0] else 0 for pos in range(10))
        else:
            self.n = n
            self.e = e
            self.s = s
            self.w = w

    def rotate(self) -> "Border":
        return Border(
            n=self.__flip(self.w),
            e=self.n,
            s=self.__flip(self.e),
            w=self.s,
        )

    def flip(self) -> "Border":
        return Border(
            n=self.s,
            e=self.__flip(self.e),
            s=self.n,
            w=self.__flip(self.w),
        )

    @staticmethod
    def __flip(num: int) -> int:
        result = 0
        for _ in range(10):
            result <<= 1
            result += num & 1
            num >>= 1
        return result

    def __str__(self):
        return f"({self.n}, {self.e}, {self.s}, {self.w})"

    def __repr__(self):
        return self.__str__()


class Tile:
    def __init__(self, number: int, pixels: List[List[bool]]):
        self.number = number
        self.pixels = pixels
        b1 = [Border(pixels=pixels)]
        b2 = [b1[0].flip()]
        for i in range(1, 4):
            b1.append(b1[i-1].rotate())
            b2.append(b2[i-1].rotate())
        self.border_variations = b1 + b2
        # will be set to variation index if used
        self.variation = None


def parse_tiles(data: List[str]) -> Iterable[Tile]:
    tile_id = None
    tile = None
    for line in data:
        if line:
            m = re.match(r"^Tile (\d+):", line)
            if m:
                if tile_id is not None:
                    yield Tile(tile_id, tile)
                tile_id = int(m.group(1))
                tile = []
            else:
                tile.append([token == "#" for token in line])
    yield Tile(tile_id, tile)


def find_next(grid: List[int], grid_size: int, tiles: List[Tile], start: int = 0, variation: int = 0) -> Optional[int]:
    index = len(grid)
    row = math.floor(index / grid_size)
    col = index % grid_size
    left = tiles[grid[index - 1]] if col != 0 else None
    top = tiles[grid[index - grid_size]] if row != 0 else None
    for i in range(start, len(tiles)):
        tile = tiles[i]
        if tile.variation is not None:
            continue
        for var in range(variation, 8):
            border = tile.border_variations[var]
            try:
                if (left is None or left.border_variations[left.variation].e == border.w) and (top is None or top.border_variations[top.variation].s == border.n):
                    tile.variation = var
                    return i
            except TypeError:
                raise
        variation = 0
    return None


def part1(data: List[str]):
    tiles = list(parse_tiles(data))
    grid = []
    size = int(math.sqrt(len(tiles)))  # 12
    while len(grid) < len(tiles):
        # print(grid)
        # for new tiles, use the first match in the list
        tile = find_next(grid, size, tiles)
        # print(tile)
        # if none was found, backtrack and pick one further down the list
        while tile is None:
            # raises IndexEror if grid is empty
            index = grid.pop()
            variation = tiles[index].variation
            tiles[index].variation = None
            if variation < 7:
                tile = find_next(grid, size, tiles, index, variation + 1)
            else:
                tile = find_next(grid, size, tiles, index + 1)
        grid.append(tile)
    print("\n".join(" ".join(str(tiles[grid[row*size+col]].number)
                             for col in range(size)) for row in range(size)))
    print()
    print(tiles[grid[0]].number * tiles[grid[size - 1]].number *
          tiles[grid[size * (size - 1)]].number * tiles[grid[size*size-1]].number)


if __name__ == "__main__":
    with open("data/20.txt") as f:
        data = f.read()
    data = data.splitlines()
    part1(data)
    # part2(data)
