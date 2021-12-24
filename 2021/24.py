from itertools import product
from functools import lru_cache

# coefficients used by subroutine (found by reading and grepping on the program text)
X = [11, 13, 11, 10, -3, -4, 12, -8, -3, -12, 14, -6, 11, -12]
Y = [14, 8, 4, 10, 14, 10, 4, 14, 1, 6, 0, 9, 13, 12]
Z = [1, 1, 1, 1, 26, 26, 1, 26, 26, 26, 1, 26, 1, 26]


def part1():
    print(''.join(map(str, run())))


def part2():
    print(''.join(map(str, run(smallest=True))))


# if you have crazy amounts of time you can use this :p
def decode(instruction, registers, input):
    # append 0 to avoid 'not enough values to unpack' for inp
    op, a, b, *_ = instruction + (0,)
    ra = registers[a]
    rb = registers[b] if b in registers else int(b)
    if op == 'inp':
        registers[a] = next(input)
    elif op == 'add':
        registers[a] = ra + rb
    elif op == 'mul':
        registers[a] = ra * rb
    elif op == 'div':
        # b is non-zero
        registers[a] = ra // rb
    elif op == 'mod':
        # a is positive and b strictly positive as per instructions
        registers[a] = ra % rb
    elif op == 'eql':
        registers[a] = int(ra == rb)
    else:
        raise ValueError()


# the search space is not too big, but calculations are cpu-intensive
# -> just cache everything
@lru_cache(maxsize=None)
def run(step=0, z=0, smallest=False):
    if step < 14:
        for w in (range(1, 10) if smallest else range(9, 0, -1)):
            if (res := run(step+1, subroutine(step, w, z), smallest)) is not None:
                return [w] + res
    else:
        return [] if z == 0 else None


# manually reading the program reveals that the same subroutine is called for every digit
# the subroutine zeroes x and y first, so only z is of relevance for the next call
# the manually simplified code is below
def subroutine(i, w, z):
    # observe that X[i] is always negative if Z[i] is 26 and > 10 if it's 1
    # -> x can never equal w in these cases
    # -> z will always increase in these 7 cases, regardless of what we do
    # you can likely construct constraints from this and feed them to a constraint solver like z3
    x = z % 26 + X[i]
    z //= Z[i]
    if x != w:
        z = 26 * z + w + Y[i]
    return z


# not actually used as the program was "decompiled" by hand, yielding the subroutine above
def read():
    with open('data/24.txt') as f:
        data = [tuple(l.strip().split(' ')) for l in f.readlines() if l.strip()]
    return data


if __name__ == '__main__':
    part1()
    part2()
