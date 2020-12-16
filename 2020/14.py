import re
"""
This one's written in Python because JS bitwise operators work on 32-bit signed integers only
See https://www.w3schools.com/js/js_bitwise.asp
"""

TESTDATA = ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
            "mem[8] = 11", "mem[7] = 101", "mem[8] = 0"]
TESTDATA2 = ["mask = 000000000000000000000000000000X1001X", "mem[42] = 100",
             "mask = 00000000000000000000000000000000X0XX", "mem[26] = 1"]


class Mask:
    def __init__(self):
        self.mask = ""
        self.or_mask = 0
        self.and_mask = 0

    def update(self, mask):
        self.mask = mask
        self.or_mask = 0
        self.and_mask = 0
        for token in mask:
            self.or_mask <<= 1
            self.and_mask <<= 1
            if token != "0":
                self.and_mask += 1
            if token == "1":
                self.or_mask += 1

    def apply_to_value(self, value):
        return (value & self.and_mask) | self.or_mask

    def apply_to_address(self, address):
        address_string = f"{address:036b}"
        masked = ""
        for index in range(36):
            if self.mask[index] == "0":
                masked += address_string[index]
            else:
                masked += self.mask[index]
        return masked


def generate_addresses(masked):
    count = masked.count("X")
    for current in range(2**count-1, -1, -1):
        bits = f"{current:0{count}b}"
        index = 0
        address = 0
        for token in masked:
            address <<= 1
            if token == "X":
                if bits[index] == "1":
                    address += 1
                index += 1
            elif token == "1":
                address += 1
        yield address


def part1():
    mask = Mask()
    mem = {}
    for instruction in read_instructions():
        if instruction[0] == "mask":
            mask.update(instruction[2])
        else:
            mem[instruction[1]] = mask.apply_to_value(int(instruction[2]))
    print(sum(mem.values()))


def part2():
    mask = Mask()
    mem = {}
    for instruction in read_instructions():
        if instruction[0] == "mask":
            mask.update(instruction[2])
        else:
            masked = mask.apply_to_address(int(instruction[1]))
            # print(masked)
            for address in generate_addresses(masked):
                mem[address] = int(instruction[2])
    print(sum(mem.values()))


def read_instructions():
    with open("data/14.txt") as f:
        data = f.readlines()
    instructions = []
    for line in data:
        m = re.match(r"^(mask|mem\[(\d+)]) = ([X0-9]*)", line)
        if m:
            instructions.append((m.group(1), m.group(2), m.group(3)))
    # print(instructions)
    return instructions


if __name__ == "__main__":
    # part1()
    part2()
