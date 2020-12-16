import re
"""
This one's written in Python because JS bitwise operators work on 32-bit signed integers only
See https://www.w3schools.com/js/js_bitwise.asp
"""

TESTDATA = ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", "mem[8] = 11", "mem[7] = 101", "mem[8] = 0"]


class Mask:
    def __init__(self):
        self.or_mask = 0
        self.and_mask = 0

    def update(self, mask):
        self.or_mask = 0
        self.and_mask = 0
        for token in mask:
            self.or_mask <<= 1
            self.and_mask <<= 1
            if token != "0":
                self.and_mask += 1
            if token == "1":
                self.or_mask += 1

    def apply(self, value):
        return (value & self.and_mask) | self.or_mask


def main():
    with open("data/14.txt") as f:
        data = f.readlines()
    instructions = []
    for line in data:
        m = re.match(r"^(mask|mem\[(\d+)]) = ([X0-9]*)", line)
        if m:
            instructions.append((m.group(1), m.group(2), m.group(3)))
    # print(instructions)
    mask = Mask()
    mem = {}
    for instruction in instructions:
        if instruction[0] == "mask":
            mask.update(instruction[2])
        else:
            mem[instruction[1]] = mask.apply(int(instruction[2]))
    print(sum(mem.values()))



if __name__ == "__main__":
    main()