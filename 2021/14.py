import math

TESTDATA = [
    'NNCB',
    '',
    'CH -> B',
    'HH -> N',
    'CB -> H',
    'NH -> C',
    'HB -> C',
    'HC -> B',
    'HN -> C',
    'NN -> C',
    'BH -> H',
    'NC -> B',
    'NB -> B',
    'BN -> B',
    'BB -> N',
    'BC -> B',
    'CC -> N',
    'CN -> C',
]


class Element:
    def __init__(self, name):
        self.__name = name
        self.__next = None

    def __iter__(self):
        el = self
        while el is not None:
            # written like this because consumers of the iterator may change __next (causing an infinite loop)
            n = el.__next
            yield el
            el = n

    def __str__(self) -> str:
        return ''.join(e.__name for e in self)

    def append(self, element):
        if self.__next is None:
            self.__next = element
        else:
            self.__next.append(element)

    def insert(self, rules):
        # can also be written with recursion, but that will rapidly exceed max depth
        for el in self:
            if el.__next is not None:
                element = Element(rules[el.__name + el.__next.__name])
                element.__next = el.__next
                el.__next = element

    def count_elements(self):
        elements = {}
        for e in self:
            name = e.__name
            if name not in elements:
                elements[name] = 1
            else:
                elements[name] += 1
        return elements


def part1():
    template, _, rules = read()
    # print(rules)
    # print(template)
    for _ in range(10):
        template.insert(rules)
        print('.', end='', flush=True)
        # print(template)
    print()
    elements = template.count_elements()
    most = max(elements, key=elements.get)
    least = min(elements, key=elements.get)
    print(elements, most, least)
    print(elements[most] - elements[least])


def part2():
    # does the same, but with 40 iterations
    # this uses way too much memory, so we can't generate the whole template as we did in part 1
    # -> keep track of the pair counts and define expansion rules
    # the trick is that since we insert, we always know the new pairs regardless of their position in the string
    _, pairs, rules = read()
    print(pairs)
    for _ in range(40):
        pairs = insert(pairs, rules)
    print(pairs)
    elements = {}
    for pair, count in pairs.items():
        add(elements, pair[0], count)
        add(elements, pair[1], count)
    most = max(elements, key=elements.get)
    least = min(elements, key=elements.get)
    print(elements, most, least)
    # all elements but head and tail are part of two pairs -> divide by 2 and round up
    print(math.ceil(elements[most] / 2) - math.ceil(elements[least] / 2))


def insert(pairs, rules):
    newpairs = {}
    for pair, count in pairs.items():
        new = rules[pair]
        add(newpairs, pair[0] + new, count)
        add(newpairs, new + pair[1], count)
    return newpairs


def read():
    with open("data/14.txt") as f:
        data = [l.strip() for l in f.readlines() if l.strip()]
    # data = [l.strip() for l in TESTDATA if l.strip()]
    template = Element(data[0][0])
    for c in data[0][1:]:
        template.append(Element(c))
    pairs = {}
    for i in range(len(data[0]) - 1):
        add(pairs, data[0][i:i+2], 1)
    rules = [l.split(' -> ') for l in data[1:]]
    # part 1 uses template, part 2 pairs
    # both approaches are kept for reference even though the pairs work best
    return template, pairs, dict(rules)


def add(d, item, count):
    if item in d:
        d[item] += count
    else:
        d[item] = count


if __name__ == '__main__':
    # part1()
    part2()
