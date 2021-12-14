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
    template, rules = read()
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
    # this uses way too much memory, so we'll need something clever...
    pass


def read():
    with open("data/14.txt") as f:
        data = [l.strip() for l in f.readlines() if l.strip()]
    # data = [l.strip() for l in TESTDATA if l.strip()]
    template = Element(data[0][0])
    for c in data[0][1:]:
        template.append(Element(c))
    rules = [l.split(' -> ') for l in data[1:]]
    return template, dict(rules)


if __name__ == '__main__':
    part1()
    part2()
