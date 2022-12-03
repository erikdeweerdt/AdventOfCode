testdata = '''
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''


class Rucksack:
    def __init__(self, contents):
        self.size = len(contents)
        self.compartment_size = self.size // 2
        self.all = set(contents)
        self.c1 = set(contents[:self.compartment_size])
        self.c2 = set(contents[self.compartment_size:])


def part1():
    total = 0
    for rucksack in read():
        total += priority(next(iter(rucksack.c1.intersection(rucksack.c2))))
    print(total)


def part2():
    total = 0
    rucksacks = list(read())
    for i in range(0, len(rucksacks), 3):
        badge = rucksacks[i].all.intersection(rucksacks[i+1].all, rucksacks[i+2].all)
        if len(badge) != 1:
            raise Exception('Badge not found')
        total += priority(next(iter(badge)))
    print(total)


def priority(item):
    p = ord(item)
    return p - 96 if p > 90 else p - 38


def read():
    with open(f'data/{__file__.replace(".py", ".txt")}') as f:
        data = list(map(str.strip, f.readlines()))
    # data = list(map(str.strip, testdata.splitlines()))
    for line in data:
        if line:
            yield Rucksack(line)


if __name__ == '__main__':
    part1()
    part2()
