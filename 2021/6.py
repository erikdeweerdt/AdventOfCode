# note: I misinterpreted the problem at first
# _every_ new generation starts at 8 and _not_ at the previous maximum + 1
# the second one is a lot harder and cost me a lot of time :p

def fishes(generations):
    with open("data/6.txt") as f:
        data = [int(l) for l in f.readline().split(',')]
    # data = [3,4,3,1,2]
    fish = [0 for _ in range(9)]
    for f in data:
        fish[f] += 1
    # print(0, fish)
    for g in range(generations):
        z = fish[0]
        for f in range(len(fish) - 1):
            fish[f] = fish[f + 1]
        fish[6] += z
        fish[8] = z
        # print(g + 1, fish)
    return sum(fish)


def part1():
    print(fishes(80))


def part2():
    print(fishes(256))


if __name__ == '__main__':
    part1()
    part2()
