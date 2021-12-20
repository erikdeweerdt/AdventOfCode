from itertools import product


def part1():
    bounds, pattern, image = read()
    image, bounds, state = enhance(pattern, image, bounds, False)
    image, bounds, state = enhance(pattern, image, bounds, state)
    # print_image(image, bounds)
    print(len(image))


def part2():
    bounds, pattern, image = read()
    state = False
    for _ in range(50):
        print('.', end='', flush=True)
        image, bounds, state = enhance(pattern, image, bounds, state)
    # print_image(image, bounds)
    print()
    print(len(image))


def enhance(pattern, image, bounds, grid_state=False):
    # should return the new image and the infinite grid's state
    # validity of the pattern was already checked, so the grid state just flips if pattern[0] == True
    new_image = set()
    new_bounds = ((bounds[0][0] - 1, bounds[0][1] - 1), (bounds[1][0] + 1, bounds[1][1] + 1))
    for x, y in product(range(new_bounds[0][0], new_bounds[1][0]), range(new_bounds[0][1], new_bounds[1][1])):
        p = 0
        for dy, dx in product(range(-1, 2, 1), repeat=2):
            p = p * 2 + int(get(x+dx, y+dy, image, bounds, grid_state))
        if pattern[p]:
            new_image.add((x, y))
    return new_image, new_bounds, grid_state ^ pattern[0]


def get(x, y, image, bounds, grid_state):
    if x < bounds[0][0] or x >= bounds[1][0] or y < bounds[0][1] or y >= bounds[1][1]:
        return grid_state
    return (x, y) in image


def print_image(image, bounds):
    for y in range(bounds[0][1], bounds[1][1]):
        print(''.join('#' if (x, y) in image else '.' for x in range(bounds[0][0], bounds[1][0])))


def read():
    with open("data/20.txt") as f:
        pattern = [c == '#' for c in f.readline().strip()]
        f.readline()
        data = list(map(str.strip, f.readlines()))
    bounds = (len(data[0]), len(data))
    image = set([(x, y) for x, y in product(range(bounds[0]), range(bounds[1])) if data[y][x] == '#'])
    # note: if pattern[0] is True (on), pattern[511] _must_ be False (off)
    # otherwise all pixels turn on and stay that way, resulting in infinity being the answer
    assert not pattern[0] or not pattern[511]
    # print(pattern)
    # print(data)
    # print(image)
    return ((0, 0), bounds), pattern, image


if __name__ == '__main__':
    # part1()
    part2()
