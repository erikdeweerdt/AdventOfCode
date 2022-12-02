def part1():
    mx = 0
    for elf in read():
        if elf > mx:
            mx = elf
    print(mx)


def part2():
    elves = sorted(read(), reverse=True)
    print(elves[0] + elves[1] + elves[2])


def read():
    with open('data/1.txt') as f:
        data = list(map(str.strip, f.readlines()))
    total = 0
    for line in data:
        if line:
            total += int(line)
        else:
            yield total
            total = 0
    yield total


if __name__ == '__main__':
    part1()
    part2()
