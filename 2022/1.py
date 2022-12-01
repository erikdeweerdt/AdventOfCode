class Elf:
    def __init__(self):
        self.__items = []
        self.__total = 0

    def add(self, item):
        self.__items.append(item)
        self.__total += item

    def get_total(self):
        return self.__total


def part1():
    mx = 0
    for elf in read():
        if elf.get_total() > mx:
            mx = elf.get_total()
    print(mx)


def part2():
    def key(elf): return elf.get_total()
    elves = sorted(list(read()), key=key, reverse=True)
    print(elves[0].get_total() + elves[1].get_total() + elves[2].get_total())


def read():
    with open('data/1.txt') as f:
        data = list(map(str.strip, f.readlines()))
    elf = None
    for line in data:
        if line:
            if elf is None:
                elf = Elf()
            elf.add(int(line))
        else:
            yield elf
            elf = None
    if elf:
        yield elf


if __name__ == '__main__':
    part1()
    part2()
