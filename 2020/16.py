import re

TESTDATA = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""".splitlines()


def parse_rules(data):
    rules = {}
    for line in data:
        match = re.match(r"^([a-z ]*): (\d+)-(\d+) or (\d+)-(\d+)", line)
        if match:
            rules[match.group(1)] = [(int(match.group(2)), int(match.group(3))),
                                     (int(match.group(4)), int(match.group(5)))]
    return rules


def parse_tickets(data):
    tickets = []
    for line in data:
        if re.match(r"^(\d+,?)+$", line):
            tickets.append([int(value) for value in line.split(",")])
    return tickets


def get_matching_classes(value, rules):
    for name, ranges in rules.items():
        for range_min, range_max in ranges:
            # ranges are inclusive
            if value >= range_min and value <= range_max:
                yield name
                break


def part1(data):
    rules = parse_rules(data)
    your_ticket, *nearby_tickets = parse_tickets(data)
    error_rate = 0
    for ticket in nearby_tickets:
        for value in ticket:
            try:
                next(get_matching_classes(value, rules))
            except StopIteration:
                error_rate += value
    print(error_rate)


if __name__ == "__main__":
    with open("data/16.txt") as f:
        data = f.read()
    data = data.splitlines()
    part1(data)
