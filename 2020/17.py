from typing import Dict, Iterable, List, Tuple

TESTDATA = """
.#.
..#
###
"""
DATA = """
#####..#
#..###.#
###.....
.#.#.#..
##.#..#.
######..
.##..###
###.####
"""


class Cube:
    def __init__(self, x: int, y: int, z: int, active=False):
        self.x = x
        self.y = y
        self.z = z
        self.active = active
        self.next = active

    def __str__(self):
        token = "#" if self.active else "."
        return f"({self.x},{self.y},{self.z})[{token}]"

    def __repr__(self):
        return self.__str__()


class PocketDimension:
    cubes: List[Cube]
    lookup: Dict[int, Dict[int, Dict[int, Cube]]]

    def __init__(self, cubes: List[Cube]):
        self.cubes = cubes
        self.lookup = {}
        self._insert_cubes(cubes)
        self._ensure_neighbors()

    def _insert_cubes(self, cubes) -> None:
        for cube in cubes:
            if cube.x not in self.lookup:
                self.lookup[cube.x] = {}
            if cube.y not in self.lookup[cube.x]:
                self.lookup[cube.x][cube.y] = {}
            self.lookup[cube.x][cube.y][cube.z] = cube

    def _ensure_neighbors(self) -> None:
        for cube in self.cubes:
            if cube.active:
                for x, y, z in PocketDimension._neighbor_range(cube):
                    try:
                        _ = self.lookup[x][y][z]
                    except KeyError:
                        new_cube = Cube(x, y, z)
                        self.cubes.append(new_cube)
                        self._insert_cubes([new_cube])

    @staticmethod
    def _neighbor_range(cube) -> Iterable[Tuple[int, int, int]]:
        for x in range(cube.x-1, cube.x+2):
            for y in range(cube.y-1, cube.y+2):
                for z in range(cube.z-1, cube.z+2):
                    if (cube.x != x or cube.y != y or cube.z != z):
                        yield (x, y, z)

    def active_neighbors(self, cube) -> int:
        active = 0
        for x, y, z in PocketDimension._neighbor_range(cube):
            try:
                if self.lookup[x][y][z].active:
                    active += 1
            except KeyError:
                pass
        return active

    def step(self) -> None:
        for cube in self.cubes:
            active = self.active_neighbors(cube)
            if cube.active:
                cube.next = active == 2 or active == 3
            else:
                cube.next = active == 3
            # if cube.z == 0:
            #     print(f"({cube.x},{cube.y},{cube.z}): {active} {cube.active} -> {cube.next}")
        for cube in self.cubes:
            cube.active = cube.next
        self._ensure_neighbors()


def make_dimension(data: str) -> PocketDimension:
    cubes = []
    y = 0
    for line in data.splitlines():
        if line:
            x = 0
            for token in line:
                cubes.append(Cube(x, y, 0, token == "#"))
                x += 1
            y += 1
    return PocketDimension(cubes)


def part1(data: str):
    dimension = make_dimension(data)
    for _ in range(6):
        dimension.step()
    # print([cube for cube in dimension.cubes if cube.active])
    print(sum(1 if cube.active else 0 for cube in dimension.cubes))


if __name__ == "__main__":
    part1(DATA)
